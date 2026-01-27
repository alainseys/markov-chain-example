#!/usr/bin/env python3
from html_sanitizer import Sanitizer
from nicegui import ui
import collections, random, sys, textwrap

def root():
    def generate():
        # Build possibles table indexed by pair of prefix words (w1, w2)
        w1 = w2 = ''
        possibles = collections.defaultdict(list)
        file = open("commedia.txt", "r")
        for line in file:
            for word in line.split():
                possibles[w1, w2].append(word)
                w1, w2 = w2, word

        # Avoid empty possibles lists at end of input
        possibles[w1, w2].append('')
        possibles[w2, ''].append('')

        # Generate randomized output (start with a random capitalized prefix)
        w1, w2 = random.choice([k for k in possibles if k[0][:1].isupper()])
        output = [w1, w2]
        for _ in range(int(100)):
            word = random.choice(possibles[w1, w2])
            output.append(word)
            w1, w2 = w2, word

        # Print output wrapped to 70 columns
        # print(output)

        print('entro')
        return textwrap.fill(' '.join(output)).rsplit('.')[0]

    async def send() -> None:
        question = text.value
        text.value = ''
        with message_container:
            print(question)
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Hogwarts Expert', sent=False)
            print(response_message)
            spinner = ui.spinner(type='dots', size='lg', color='primary')

        await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        response = ''
        response = generate()
        print(response)
        print(response_message)
        with response_message.clear():
            print(response)
            ui.html(response, sanitize=Sanitizer().sanitize)
            await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)

    message_container = ui.column().classes('w-full max-w-2xl mx-auto flex-grow items-stretch')

    with (ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6')):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'Message'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3').classes('w-full self-center').on('keydown.enter', send)
            button = ui.button(text="Send", color="primary", on_click=send).props('rounded outlined input-class=mx-3').classes('self-center')

        ui.markdown('Made with 🔥 by [carmelolg](https://carmelolg.github.io)') \
            .classes('text-xs self-center mr-12 m-[-1em] text-primary') \
            .classes('[&_a]:text-inherit [&_a]:no-underline [&_a]:font-medium')


ui.run(root, title='Hogwarts Spell Chatbot', favicon='🪄', show_welcome_message=True, reconnect_timeout=60)
