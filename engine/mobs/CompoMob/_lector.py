from ._animado import Animado
from engine.misc.resources import combine_mob_spritesheets
from engine.globs.mod_data import ModData
from engine.globs.tiempo import Tiempo


class Lector(Animado):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus = 80
        self.interest = 70
        self.language_skill = 0
        self.related_skill = 4
        self.current_skill = 0
        self.reading_progress = {}  # {book_id: words_read}

        heads = ModData.graphs + 'mobs/imagenes/heads_reading_heroe.png'
        bodies = ModData.graphs + 'mobs/imagenes/heroe_reading_body.png'
        self.reading_anims = dict(zip(['abajo', 'arriba', 'izquierda', 'derecha'],
                                      combine_mob_spritesheets(heads, bodies)))

    # -------------------------
    # VELOCIDAD DE LECTURA
    # -------------------------
    def reading_speed(self, book):
        base_wpm = 200
        language_factor = self.language_skill / (self.language_skill + 5)
        mental_factor = ((0.5 + self.focus / base_wpm) * (0.5 + self.interest / base_wpm))

        effective_difficulty = (book.difficulty + book.technicality - (self.language_skill + 0.5 * self.related_skill))
        effective_difficulty = max(-50, effective_difficulty)
        difficulty_factor = 1 / (1 + effective_difficulty / 100)

        speed = base_wpm * mental_factor * difficulty_factor * language_factor
        return speed  # palabras por minuto

    # -------------------------
    # GANANCIA TOTAL SI TERMINA
    # -------------------------
    def skill_gain_total(self, book):
        k = book.difficulty
        x = self['Inteligencia']  # 10
        return book.quality * (x / (x + k)) * (1 - self.current_skill / 100) * (self.interest / 100)

    # -------------------------
    # GANANCIA PROPORCIONAL
    # -------------------------
    def skill_gain_progress(self, delta_words, book):
        total_gain = self.skill_gain_total(book)
        delta_ratio = delta_words / book.words
        return total_gain * delta_ratio

    def read(self, book, delta_minutes):
        self.detener_movimiento()
        for effect in book.on_read_tick:
            effect.apply(self)
        speed = self.reading_speed(book)
        words = speed * delta_minutes

        current = self.reading_progress.get(book.id, 0)
        new_total = min(book.words, current + words)
        self.reading_progress[book.id] = new_total

        # aplicar skill proporcional
        delta_words = new_total - current
        gain = self.skill_gain_progress(delta_words, book)
        self.current_skill += gain

        # si terminó
        if new_total >= book.words:
            self.finish_book(book)

    def consult(self, book, minutes):
        familiarity = self.reading_progress.get(book.id, {}).get("familiarity", 0)

        gain = book.quality * 0.01 * (1 - familiarity)
        familiarity += 0.05 * minutes

        self.reading_progress[book.id] = {
            "familiarity": min(1.0, familiarity),
            "last_used": Tiempo.clock.timestamp()
        }

        return gain

    def open_book(self, book):
        for effect in book.on_open:
            effect.apply(self)

    def finish_book(self, book):
        for effect in book.on_finish:
            effect.apply(self)