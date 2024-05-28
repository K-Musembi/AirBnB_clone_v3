#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

states = list(storage.all(State).values())
if states:
    first_state_id = states[0].id
    print("First state: {}".format(storage.get(State, first_state_id)))
else:
    print("No states found in database")
