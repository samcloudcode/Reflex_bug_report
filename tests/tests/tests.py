"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from typing import List, Dict
import json

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    my_var: str = 'Hello'
    my_list: List[str] = ['Hello', 'Goodbye!']
    my_bools: List[bool] = [True, False]
    saved_json: str = ""
    j: int = 0

    def update_list(self, i, value):
        self.my_list[int(i)] = value

    def update_bools(self, i, value):
        self.my_bools[int(i)] = value

    def add_list_item(self):
        self.my_list.append('')

    def add_bools_item(self):
        self.my_bools.append(False)

    def save_to_json(self):
        data_dict = {
            'my_list': self.my_list,
            'my_bools': self.my_bools,
        }

        self.saved_json = json.dumps(data_dict)

    def retrieve_from_json(self):
        if self.saved_json:
            data_dict = json.loads(self.saved_json)

            # We should ensure that the data retrieved is in the correct format before assigning
            if 'my_list' in data_dict and isinstance(data_dict['my_list'], list):
                self.my_list = data_dict['my_list']

            if 'my_bools' in data_dict and isinstance(data_dict['my_bools'], list):
                self.my_bools = data_dict['my_bools']



def input_box(text: str, i: int):
    return rx.box(
        rx.text("Item: " + i),
        rx.text("Content: " + text),
        rx.text("Value + On Change:"),
        rx.input(placeholder='Test',
                 value=State.my_list[i],
                 on_change=lambda value: State.update_list(i, value),
                 ),
        rx.text("Default_Value + On Blur:"),
        rx.input(placeholder='Test',
                 default_value=State.my_list[i],
                 on_blur=lambda value: State.update_list(i, value),
                 ),
        width='30em',
        padding_top='3em'
    )


def check_box(state: str, i: int):
    return rx.box(
        rx.text("Item: " + i),
        rx.text("State: " + state),
        rx.checkbox(i, is_checked=State.my_bools[i], on_change=lambda value: State.update_bools(i, value)),
        width='30em',
        padding_top='3em'
    )

def index():
    return rx.fragment(
        rx.heading('Single string var', padding_top='3em'),
        rx.text("Content: " + State.my_var),
        rx.text("Value + On Change:"),
        rx.input(placeholder='Test',
                 value=State.my_var,
                 on_change=lambda value: State.set_my_var,
                 ),
        rx.text("Default_Value + On Blur:"),
        rx.input(placeholder='Test',
                 default_value=State.my_var,
                 on_blur=lambda value: State.set_my_var,
                 ),

        rx.heading('List of string vars', padding_top='3em'),

        rx.foreach(
            State.my_list,
            lambda text, index: input_box(text, index),
        ),
        rx.foreach(
            State.my_bools,
            lambda state, index: check_box(state, index),
        ),
        rx.text(State.saved_json),
        rx.button(
            'Add List item',
            on_click=State.add_list_item,
        ),
        rx.button(
            'Add Bool item',
            on_click=State.add_bools_item,
        ),
        rx.button(
            'Save to json',
            on_click=State.save_to_json,
        ),
        rx.button(
            'Retrieve from json',
            on_click=State.retrieve_from_json,
        ),

        rx.heading('Single text field for updating list', padding_top='3em'),
        rx.input(on_change=State.set_j),
        rx.text(State.j),
        rx.text("Content: " + State.my_list[State.j]),
        rx.text("Value + On Change:"),
        rx.input(placeholder='Test',
                 value=State.my_list[State.j],
                 on_change=lambda value: State.update_list(State.j, value),
                 ),
        rx.text("Default_Value + On Blur:"),
        rx.input(placeholder='Test',
                 default_value=State.my_list[State.j],
                 on_blur=lambda value: State.update_list(State.j, value),
                 ),
    )

# Add state and page to the app.
app = rx.App(state=State)
app.add_page(index)
app.compile()
