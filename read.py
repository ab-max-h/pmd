from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from fractions import Fraction

class MDSeparator(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.size_hint_y = None
        self.height = dp(1)

    def on_size(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.scroll = ScrollView()
        self.form_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        self.tipo_problema = MDTextField(
            hint_text="Tipo de problema ('max' o 'min')",
            helper_text="Debe ser 'max' o 'min'",
            helper_text_mode="on_error"
        )

        self.num_estados = MDTextField(
            hint_text="Número de estados",
            input_filter='int',
            helper_text="Solo números enteros",
            helper_text_mode="on_error"
        )

        self.num_decisiones = MDTextField(
            hint_text="Número de decisiones",
            input_filter='int',
            helper_text="Solo números enteros",
            helper_text_mode="on_error"
        )

        self.form_layout.add_widget(MDLabel(
            text="Configuración inicial:",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)))

        self.form_layout.add_widget(self.tipo_problema)
        self.form_layout.add_widget(self.num_estados)
        self.form_layout.add_widget(self.num_decisiones)

        self.boton_continuar = MDRaisedButton(
            text="Continuar",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(150, 50),
            on_release=self.validar_datos
        )
        self.form_layout.add_widget(self.boton_continuar)

        self.scroll.add_widget(self.form_layout)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def validar_datos(self, instance):
        try:
            problema_tipo = self.tipo_problema.text.strip().lower()
            if problema_tipo not in ['max', 'min']:
                raise ValueError("Tipo de problema inválido")

            num_estados = int(self.num_estados.text)
            num_decisiones = int(self.num_decisiones.text)

            MDApp.get_running_app().datos = {
                'problema_tipo': 'Maximizar' if problema_tipo == 'max' else 'Minimizar',
                'num_estados': num_estados,
                'num_decisiones': num_decisiones,
                'politicas': {},
                'costos': {},
                'probabilidades': {}
            }

            self.manager.current = 'politicas'

        except Exception as e:
            self.tipo_problema.error = True
            self.tipo_problema.helper_text = str(e)

class PoliticasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.scroll = ScrollView()
        self.form_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))
        self.entries = []

        self.scroll.add_widget(self.form_layout)
        self.layout.add_widget(MDLabel(
            text="Políticas disponibles:",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)))

        self.layout.add_widget(self.scroll)

        self.boton_continuar = MDRaisedButton(
            text="Siguiente",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(150, 50),
            on_release=self.procesar_politicas
        )
        self.layout.add_widget(self.boton_continuar)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.form_layout.clear_widgets()
        self.entries.clear()
        app = MDApp.get_running_app()
        for j in range(1, app.datos['num_decisiones'] + 1):
            self.form_layout.add_widget(MDLabel(
                text=f"Decisión {j}:",
                theme_text_color="Primary",
                font_style="H6",
                size_hint_y=None,
                height=dp(30)))

            entrada = MDTextField(
                hint_text=f"Estados (ej: 0,1,2)",
                helper_text="Separar con comas",
                helper_text_mode="persistent"
            )
            self.entries.append((j, entrada))
            self.form_layout.add_widget(entrada)

    def procesar_politicas(self, instance):
        app = MDApp.get_running_app()
        try:
            politicas = {}
            for j, entrada in self.entries:
                estados = [int(e.strip()) for e in entrada.text.split(',') if e.strip()]
                if not estados:
                    raise ValueError(f"Decisión {j} no tiene estados")
                politicas[j] = estados

            app.datos['politicas'] = politicas
            self.manager.current = 'costos'

        except Exception as e:
            entrada.error = True
            entrada.helper_text = str(e)

class CostosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.scroll = ScrollView()
        self.form_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))
        self.entries = []

        self.scroll.add_widget(self.form_layout)
        self.layout.add_widget(MDLabel(
            text="Costos asociados:",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)))

        self.layout.add_widget(self.scroll)

        self.boton_continuar = MDRaisedButton(
            text="Siguiente",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(150, 50),
            on_release=self.procesar_costos
        )
        self.layout.add_widget(self.boton_continuar)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.form_layout.clear_widgets()
        self.entries.clear()
        app = MDApp.get_running_app()

        for j in app.datos['politicas']:
            for i in app.datos['politicas'][j]:
                label = MDLabel(
                    text=f"Costo c_{{{i},{j}}}",
                    theme_text_color="Primary",
                    size_hint_y=None,
                    height=dp(30))

                entrada = MDTextField(
                    hint_text="Ej: 1/3 o 0.25",
                    helper_text="Valor o fracción",
                    helper_text_mode="persistent"
                )

                self.entries.append((i, j, entrada))
                self.form_layout.add_widget(label)
                self.form_layout.add_widget(entrada)

    def procesar_costos(self, instance):
        app = MDApp.get_running_app()
        costos = {j: {} for j in app.datos['politicas']}
        ultimo_entrada = None

        try:
            for i, j, entrada in self.entries:
                ultimo_entrada = entrada
                value = entrada.text.strip()
                if '/' in value:
                    costos[j][i] = float(Fraction(value))
                else:
                    costos[j][i] = float(value)

            app.datos['costos'] = costos
            self.manager.current = 'probabilidades'

        except Exception as e:
            if ultimo_entrada:
                ultimo_entrada.error = True
                ultimo_entrada.helper_text = str(e)

class ProbabilidadesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.scroll = ScrollView()
        self.form_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))
        self.entries = []

        self.scroll.add_widget(self.form_layout)
        self.layout.add_widget(MDLabel(
            text="Probabilidades de transición:",
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(50)))

        self.layout.add_widget(self.scroll)

        self.boton_continuar = MDRaisedButton(
            text="Finalizar",
            pos_hint={"center_x": 0.5},
            size_hint=(None, None),
            size=(150, 50),
            on_release=self.procesar_probabilidades
        )
        self.layout.add_widget(self.boton_continuar)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.form_layout.clear_widgets()
        self.entries.clear()
        app = MDApp.get_running_app()
        num_estados = app.datos['num_estados']

        for j in app.datos['politicas']:
            self.form_layout.add_widget(MDLabel(
                text=f"Decisión {j}:",
                font_style="H6",
                theme_text_color="Primary",
                size_hint_y=None,
                height=dp(30)))

            for i in app.datos['politicas'][j]:
                label = MDLabel(
                    text=f"Estado {i} → ...",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(25))

                entrada = MDTextField(
                    hint_text=f"Probabilidades (ej: 0.5, 1/2, ...)",
                    helper_text=f"{num_estados} valores separados por comas",
                    helper_text_mode="persistent"
                )

                self.entries.append((i, j, entrada))
                self.form_layout.add_widget(label)
                self.form_layout.add_widget(entrada)

    def procesar_probabilidades(self, instance):
        app = MDApp.get_running_app()
        probabilidades = {}
        num_estados = app.datos['num_estados']
        ultimo_entrada = None

        try:
            for j in app.datos['politicas']:
                matriz = []
                for i in app.datos['politicas'][j]:
                    entrada = next(e for (i_e, j_e, e) in self.entries if i_e == i and j_e == j)
                    ultimo_entrada = entrada
                    valores = entrada.text.split(',')

                    if len(valores) != num_estados:
                        raise ValueError(f"Se requieren {num_estados} valores")

                    fila = []
                    for v in valores:
                        if '/' in v.strip():
                            fila.append(float(Fraction(v.strip())))
                        else:
                            fila.append(float(v.strip()))

                    matriz.append(fila)

                probabilidades[j] = matriz

            app.datos['probabilidades'] = probabilidades
            self.manager.current = 'resumen'

        except Exception as e:
            if ultimo_entrada:
                ultimo_entrada.error = True
                ultimo_entrada.helper_text = str(e)

class ResumenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.layout = MDBoxLayout(orientation="vertical")
        self.scroll = ScrollView()
        self.content = MDBoxLayout(orientation="vertical", size_hint_y=None, spacing=20, padding=40)
        self.content.bind(minimum_height=self.content.setter('height'))
        self.scroll.add_widget(self.content)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def on_enter(self):
        self.content.clear_widgets()
        app = MDApp.get_running_app()

        self.content.add_widget(self.crear_tarjeta(
            titulo="CONFIGURACIÓN DEL PROBLEMA",
            contenido=[
                ("Tipo de problema:", app.datos['problema_tipo']),
                ("Número de estados:", str(app.datos['num_estados'])),
                ("Número de decisiones:", str(app.datos['num_decisiones']))
            ]
        ))

        politicas = [(f"Decisión {j}", ", ".join(map(str, estados))) for j, estados in app.datos['politicas'].items()]
        self.content.add_widget(self.crear_tarjeta(
            titulo="POLÍTICAS DEFINIDAS",
            contenido=politicas
        ))

        costos = []
        for j in app.datos['costos']:
            for i in app.datos['costos'][j]:
                costos.append((f"c_{i},{j}", f"{app.datos['costos'][j][i]:.4f}"))
        self.content.add_widget(self.crear_tarjeta(
            titulo="COSTOS ASOCIADOS",
            contenido=costos
        ))

        for j in app.datos['probabilidades']:
            matriz = []
            for i, fila in enumerate(app.datos['probabilidades'][j]):
                fila_str = " | ".join(f"{v:.4f}" for v in fila)
                matriz.append((f"Estado {i}", fila_str))

            self.content.add_widget(self.crear_tarjeta(
                titulo=f"MATRIZ DE TRANSICIÓN - DECISIÓN {j}",
                contenido=matriz
            ))

    def crear_tarjeta(self, titulo, contenido):
        card = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=15,
            padding=20,
            md_bg_color=self.app.theme_cls.bg_light,
            radius=[15],
            adaptive_height=True
        )

        card.add_widget(MDLabel(
            text=f"[b]{titulo}[/b]",
            markup=True,
            halign="center",
            font_style="H6",
            size_hint_y=None,
            height=dp(40)))

        card.add_widget(MDSeparator())

        for etiqueta, valor in contenido:
            fila = MDBoxLayout(
                orientation="horizontal",
                adaptive_height=True,
                spacing=20,
                padding=(10, 5)
            )
            fila.add_widget(MDLabel(
                text=f"[b]{etiqueta}[/b]",
                markup=True,
                size_hint_x=0.4,
                theme_text_color="Primary"))
            fila.add_widget(MDLabel(
                text=valor,
                size_hint_x=0.6,
                theme_text_color="Secondary"))
            card.add_widget(fila)

        return card

class MarkovApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.sm = ScreenManager()
        self.sm.add_widget(InputScreen(name='input'))
        self.sm.add_widget(PoliticasScreen(name='politicas'))
        self.sm.add_widget(CostosScreen(name='costos'))
        self.sm.add_widget(ProbabilidadesScreen(name='probabilidades'))
        self.sm.add_widget(ResumenScreen(name='resumen'))
        return self.sm

if __name__ == '__main__':
    MarkovApp().run()
