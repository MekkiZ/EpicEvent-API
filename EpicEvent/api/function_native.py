
def create_event(request, Event, get_object_or_404, EventStatus, Client, User):
    event = Event.objects.create(
        note=request.data['note'],
        event_date=(request.data['event_date']),
        attendees=request.data['attendees'],
        date_created=request.data['date_created'],
        date_update=request.data['date_update'],
        event_statu=get_object_or_404(EventStatus, id=request.data['event_statu']),
        client=get_object_or_404(Client, id=request.data['client']),
        support_contact=get_object_or_404(User, id=request.data['support_contact']),
    )
    event.save()
    return event
