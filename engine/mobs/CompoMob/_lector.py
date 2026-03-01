from ._animado import Animado
from engine.misc.resources import combine_mob_spritesheets
from engine.globs.mod_data import ModData
from engine.globs.tiempo import Tiempo


class Lector(Animado):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.focus = 80
        self.interest = 70
        self.language_skill = 60
        self.related_skill = 40
        self.intelligence = 65
        self.current_skill = 30
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

        mental_factor = (
                (0.5 + self.focus / 200) *
                (0.5 + self.interest / 200))

        effective_difficulty = (book.difficulty + book.technicality - (self.language_skill + 0.5 * self.related_skill))
        effective_difficulty = max(-50, effective_difficulty)
        difficulty_factor = 1 / (1 + effective_difficulty / 100)

        speed = base_wpm * mental_factor * difficulty_factor
        return speed  # palabras por minuto

    # -------------------------
    # GANANCIA TOTAL SI TERMINA
    # -------------------------
    def skill_gain_total(self, book):
        return book.quality * (self.intelligence / 100) * (1 - self.current_skill / 100) * (self.interest / 100)

    # -------------------------
    # GANANCIA PROPORCIONAL
    # -------------------------
    # def skill_gain_progress(self, words_read, book):
    #     total_gain = self.skill_gain_total(book)
    #     progress_ratio = words_read / book.words
    #     return total_gain * progress_ratio

    def read(self, book, delta_minutes):
        self.detener_movimiento()
        for effect in book.on_read_tick:
            effect.apply(self)
        speed = self.reading_speed(book)
        words = speed * delta_minutes

        current = self.reading_progress.get(book.id, 0)
        new_total = min(book.words, current + words)

        if book.id not in self.reading_progress:
            self.reading_progress[book.id] = new_total
        else:
            self.reading_progress[book.id] += new_total

        # aplicar skill proporcional
        progress_ratio = new_total / book.words
        gain = self.skill_gain_total(book) * progress_ratio
        self.current_skill += gain

        # si terminó
        if new_total >= book.words:
            self.finish_book(new_total, book)

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

    def finish_book(self, new_total, book):
        if new_total >= book.words:
            for effect in book.on_finish:
                effect.apply(self)