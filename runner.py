import random
from time import sleep

from html_sanitizer import Sanitizer
from nicegui import ui
from lib.MarkovGenerator import MarkovGenerator


def root():
    async def send() -> None:
        question = text.value
        text.value = ''
        with message_container:
            ui.add_head_html('''
                        <style>
                            .bullet-user .q-message-text {
                                background-color: #8FBE83;
                            }
                            .bullet-user .q-message-text:last-child:before {
                                border-bottom-color: #8FBE83;
                                text-color: white;
                            }
                            .bullet-ai .q-message-text {
                                background-color: #C4724F;
                            }
                            .bullet-ai .q-message-text:last-child:before {
                                border-bottom-color: #C4724F;
                                text-color: white;
                            }
                        </style>
                        ''')
            ui.chat_message(text=question, name='You', sent=True).classes('bullet-user')
            response_message = ui.chat_message(name='Anti-Agent', sent=False).classes('bullet-ai')
            spinner = ui.spinner(type='dots', size='lg', color='primary')

        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        response = MarkovGenerator.run()
        sleep(random.choice([0.5, 1, 1.5, 2]))  # Simulate thinking time
        with response_message.clear():
            ui.html(response, sanitize=Sanitizer().sanitize)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    message_container = ui.column().classes('w-full max-w-2xl mx-auto flex-grow items-stretch')

    with (ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6')):
        ui.add_head_html('''
                <style>
                    .filigrana {
                        color: #8FBE83 !important;
                        border-color: #8FBE83 !important;
                    }
                </style>
                ''')
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'Message'
            text = ui.input(placeholder=placeholder).props('outlined input-class=mx-3').classes(
                'w-full self-center filigrana').on('keydown.enter', send)
            button = ui.button(text="Send", color="primary", on_click=send).props('outlined input-class=mx-3 filigrana').classes(
                'self-center')

        ui.markdown('Designed with ❤️ by [carmelolg](https://carmelolg.github.io)') \
            .classes('text-xs self-center mr-12 m-[-1em] text-primary') \
            .classes('[&_a]:text-inherit [&_a]:no-underline [&_a]:font-medium')


ui.run(root, title='Anti Agent Chatbot', favicon='', show_welcome_message=True, reconnect_timeout=60)
