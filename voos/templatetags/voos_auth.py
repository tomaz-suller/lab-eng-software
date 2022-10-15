from typing import Callable

from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter
def can_view(user: User, page: str) -> bool:
    page_view_function_map: dict[str, Callable[[User], bool]] = {
        "crud": can_view_crud,
        "movimentacao": can_view_movimentacao,
        "relatorio": can_view_relatorio,
    }
    return page_view_function_map[page.lower()](user)


def can_view_crud(user: User) -> bool:
    return any(
        (
            user.has_perm(f"voos.view_{model}")
            for model in [
                "companhia_aerea",
                "estado",
                "instancia_voo",
                "movimentacao",
                "voo",
            ]
        )
    )


def can_view_movimentacao(user: User) -> bool:
    return user.has_perm("voos.view_movimentacao")


def can_view_relatorio(user: User) -> bool:
    return user.groups.filter(name__in=["gerente", "admin"]).exists()
