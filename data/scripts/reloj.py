def on_hora(event):
    """
    :param event:
    :type event:GiftEvent
    :return:
    """
    print('Reloj dice: son las '+str(event.data['hora'])+' hs!')
