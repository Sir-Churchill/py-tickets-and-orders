from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket.get("movie_session"))
            tickets_created = Ticket(
                movie_session=movie_session,
                order=order,
                row=ticket.get("row"),
                seat=ticket.get("seat"))

            tickets_created.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
