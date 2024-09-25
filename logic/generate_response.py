from openai import OpenAI
from typing import Literal
from .bot_funcs import send_emails
import json
from decouple import config
import openai

initial_role = f"""
{config('initial_role')}
"""

key = str(config('GPT'))

client = OpenAI(api_key=key,)



add_func_properties = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of user"
        },
        "message": {
            "type": "string",
            "description": "message of user"
        },
        "email_of_customer": {
            "type": "string",
            "description":f"email of user, e.g example@gmail.com"
        }
    },
    "required": ["name", 'message', "email_of_customer"]
}


tools = [
        {
            "type": "function",
            "function": {
                "name": "send_emails",
                "description": "send techinical email andreyabout new orders",
                "parameters": add_func_properties
            },
        },
    ]

start_sys_message = """
Не делайте предположений о том, какие значения использовать в функциях. 
Запрашивайте разъяснения, если запрос пользователя не ясен. 
Убедитесь, что ввод пользователя для имён и адресов электронной почты корректен, прежде чем продолжить. 
В частности, имена должны быть проверены, чтобы убедиться, 
что это обычные человеческие имена, а не другие существительные или фразы. 
Если ввод неясен или не соответствует критериям, запросите у пользователя уточнение. 
Убедитесь, что имя отправителя — нормальное имя. Если имя не является обычным именем 
(например, фрукт, овощ, животное, объект или термин, который не является именем), 
запросите у пользователя заменить его на обычное человеческое имя, пока он не предоставит его. 
Подтвердите, что адрес электронной почты получателя имеет правильный формат, не example@ или fake@. 
Если нет, попросите пользователя предоставить действительный адрес электронной почты. 
Сообщайте о полях, таких как имя, электронная почта и сообщение. 
Говорите об ограничениях только в случае, если введены недопустимые данные для полей. 
Все ответы должны быть на русском или казахском языках. 
На вопросы, такие как "Где вы работаете?", сначала укажите название компании, а затем — ограничения по местоположению. Например, укажите, что компания работает в городах Алматы, Талгар и Каскелен.
Ответы долдны быть короткими
For more detailed information  tell to call use our phone number is +77719333330 this number also has a whatsapp
this website in header has address as link in google maps the address Каирбекова 70,
and 3 icons links phone, whatsapp, telegram, they go in this order, and nothing more in the header


### **Services and approximate Pricing tell is not exact price if asked how to get the exact price tell call us, then our engineer will inspect the place to tell the exact amount:

Ajax and Raptor have a mobile app, Ajax app has more options to control the security systems.


**Flat Security:**
- 1-room flat: 
  - Ajax: 148k KZT, 
  - Paradox (wired): 51k KZT, 
  - Paradox (wireless): 130k KZT, 
  - Raptor: 111k KZT, 
  - Stemax: 145k KZT
- 2-room flat: 
  - Ajax: 167k KZT, 
  - Paradox (wired): 61k KZT, 
  - Paradox (wireless): 155k KZT, 
  - Raptor: 129k KZT, 
  - Stemax: 170k KZT
- 3-room flat: 
  - Ajax: 186k KZT, 
  - Paradox (wired): 71k KZT, 
  - Paradox (wireless): 180k KZT, 
  - Raptor: 147k KZT, 
  - Stemax: 195k KZT
- 4-room flat: 
  - Ajax: 205k KZT, 
  - Paradox (wired): 81k KZT, 
  - Paradox (wireless): 205k KZT, 
  - Raptor: 165k KZT, 
  - Stemax: 220k KZT

**Emergency Button (Тревожная сигнализация):**
- Stationary button: 1k KZT
- Wireless buttons (2 units): 26k KZT

**House Security:**
- Monthly fee from 10,000 KZT
- 1-room house: 
  - Ajax: 129k KZT, 
  - Paradox (wired): 45k KZT, 
  - Paradox (wireless): 105k KZT, 
  - Raptor: 93k KZT, 
  - Stemax: 120k KZT
- 2-room house: 
  - Ajax: 148k KZT, 
  - Paradox (wired): 55k KZT, 
  - Paradox (wireless): 130k KZT, 
  - Raptor: 111k KZT, 
  - Stemax: 145k KZT
- 3-room house: 
  - Ajax: 167k KZT, 
  - Paradox (wired): 65k KZT, 
  - Paradox (wireless): 155k KZT, 
  - Raptor: 129k KZT, 
  - Stemax: 170k KZT
- 4-room house: 
  - Ajax: 186k KZT, 
  - Paradox (wired): 75k KZT, 
  - Paradox (wireless): 180k KZT, 
  - Raptor: 147k KZT, 
  - Stemax: 195k KZT

**Office Security:**
- Monthly fee from 13,000 KZT
- Entry group: 
  - Ajax: 110k KZT, 
  - Paradox (wired): 35k KZT, 
  - Paradox (wireless): 80k KZT, 
  - Raptor: 75k KZT, 
  - Stemax: 95k KZT
- 1-room office: 
  - Ajax: 129k KZT, 
  - Paradox (wired): 45k KZT, 
  - Paradox (wireless): 105k KZT, 
  - Raptor: 93k KZT, 
  - Stemax: 120k KZT
- 2-room office: 
  - Ajax: 148k KZT, 
  - Paradox (wired): 55k KZT, 
  - Paradox (wireless): 130k KZT, 
  - Raptor: 111k KZT, 
  - Stemax: 145k KZT
- 3-room office: 
  - Ajax: 167k KZT, 
  - Paradox (wired): 65k KZT, 
  - Paradox (wireless): 155k KZT, 
  - Raptor: 129k KZT, 
  - Stemax: 170k KZT
- 4-room office: 
  - Ajax: 186k KZT, 
  - Paradox (wired): 75k KZT, 
  - Paradox (wireless): 180k KZT, 
  - Raptor: 147k KZT, 
  - Stemax: 195k KZT

"""



def generate_response(user_question, prev_question=None):

    messages = []

    messages.append(
        {"role": "system", "content": start_sys_message} )

    if not prev_question:
        messages.append(
            {
                "role": "assistant",
                "content": initial_role,
            }
        )
    else:
        messages.extend(prev_question)

    messages.append({"role": "user", "content": user_question})

    try:

        tool_call_details = {
            "name": None,
            "arguments": ""
        }

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=True
        )

        response_message = 'response is'

        message_id = None

        for chunk in response:

            if chunk.choices[0].delta.content is not None:
                
                yield chunk

                response_message += chunk.choices[0].delta.content

            if chunk.choices[0].delta.tool_calls:

                for tool_call in chunk.choices[0].delta.tool_calls:

                    if message_id is None and tool_call.id:
                        message_id = tool_call.id

                    if tool_call.function.name is not None:

                        tool_call_details["name"] = tool_call.function.name

                tool_call_details["arguments"] += tool_call.function.arguments

        
        if tool_call_details["name"] is not None:
            
            available_functions = {
                "send_emails": send_emails,
            }

            response_messages = {
                    "content": response_message,
                    "role": "assistant",
                    "tool_calls": [{
                        "id": message_id,
                        "tool_call_id": message_id,
                        "function": {
                            "arguments": tool_call_details["arguments"],
                            "name": tool_call_details["name"]
                        },
                        "type": "function"
                    }]
                }
                
            messages.append(response_messages)

            function_name = tool_call_details["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call_details["arguments"])
            
            if function_name == "send_emails":
                function_response = function_to_call(
                    name=function_args.get("name"),
                    message=function_args.get("message"),
                    email_of_customer=function_args.get("email_of_customer")
                )

            messages.append(
                {
                    "role": "tool",
                    "name": function_name,
                    'tool_call_id': message_id,
                    "content": f'the response:{function_response}',
                }
            )


            follow_up_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True
            )


            for chunk in follow_up_response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk

    except Exception as e:
        print(f"Error generating response: {e}")
        yield f"I'm sorry, I couldn't process your request right now. the error {e}"