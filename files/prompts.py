from files.prompt import Prompt

# Pharmacy

person = {
    "first": "Christian",
    "last": "Persson",
    "prescription": {"medicine": "Sertraline Teva, 50 mg", "usage": "75 mg (1.5 pill) every morning"}
}

place = {
    "name": "Pharmacy",
    "in stock": {"Sertraline Teva, 50 mg": {"price": "8 dollar", "qty": 5},
                 "Sertraline Sun, 50 mg": {"price": "7 dollar", "qty": 10}, "Bag": {"price": "1 dollar", "qty": 200}}
}

task = (
    "Greet the customer",
    "Check the customers id",
    "Check for prescriptions in the computer"
    "If you find a prescription, ask the customer if it's what he/she came for",
    "Check if the medicine is in stock",
    "Also check for alternatives",
    "Inform the customer about usage",
    "Put a label with information about usage on the package",
    "Ask if the customer would like a bag",
    "Calculate the grand total and inform the customer",
    "Point the customer towards the payment terminal"
)

basic_instructions = ["You are a pharmacist helping customers in a pharmacy"]

values = {
    "person": person,
    "place": place,
    "task": task,
    "basic_instructions": basic_instructions
}

pharmacy_prompt = Prompt(values).get_instructions()
