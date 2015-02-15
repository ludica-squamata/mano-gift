def on_hora(self, event):
    """
    :param event:
    :type event:GiftEvent
    :return:
    """
    print('Reloj dice: son las '+str(event.data['hora'])+' en punto!')
