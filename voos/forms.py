from django import forms

from .models import InstanciaVoo


def _departure_after_arrival(departure, arrival):
    return (
        departure and arrival
        and departure > arrival
    )


class InstanciaVooForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        for time_type in ("prevista", "real"):
            departure = cleaned_data.get(f"partida_{time_type}")
            arrival = cleaned_data.get(f"chegada_{time_type}")

            if _departure_after_arrival(departure, arrival):
                for field in ("partida", "chegada"):
                    self.add_error(
                        f"{field}_{time_type}",
                        "Horário de partida precisa ser anterior ao horário de chegada"
                    )

    class Meta:
        model = InstanciaVoo
        fields = []


class InstanciaVooCreateForm(InstanciaVooForm):

    class Meta:
        model = InstanciaVoo
        fields = [
            "partida_prevista",
            "chegada_prevista",
            "voo",
        ]


class InstanciaVooUpdateForm(InstanciaVooForm):

    class Meta:
        model = InstanciaVoo
        fields = [
            "partida_prevista",
            "chegada_prevista",
            "partida_real",
            "chegada_real",
        ]
