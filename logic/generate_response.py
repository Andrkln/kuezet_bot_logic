from openai import OpenAI
from typing import Literal
from .bot_funcs import send_emails
import json
from decouple import config

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
our office working hours between 8 a.m and 5 p.m 
and 3 icons links phone, whatsapp, telegram, they go in this order, and nothing more in the header
when tell about name usage, tell about as normal names do not tell human name

### **Services and approximate Pricing tell is not exact price if asked how to get the exact price tell call us, then our engineer will inspect the place to tell the exact amount:

Ajax and Raptor have a mobile app, Ajax app has more options to control the security systems. Ajax app has a better design, shows detailed info about each part of the 
security system. Raptor shows only general info about of turing on and off the security system and allows to turn it on and off by the app

Except for Ajax and Raptor we offer Stimax, Pardox and SKlink


our prices:
1. Квартиры 7000 тг в месяц
2. Дома  10000 тг в месяц
3. Для бизнеса от 15000 тг в месяц, to get exact price call us

the security equipment is free for custmer

Only possible cases when a customer can call to 'пульт':
1. Customer has struggles with turning security system
2. Change code for security system
3. get info about is  объект под охраной или нет
3. struggles with the app
4. on keyboard of the security system lighting numbers is on, горят цифры


If asked why you or why Kuzet standard:
1. We have our own center of monitoring and own security groups (called экипажи кузет)
2. Our security groups arrive faster than others, 5-7 minutes average arriving time
3. 20 years of experience on the market, we are one of market leaders
4. Наши охраники самые опытные
5. Мы гарантируем высшее качество безопастности
6. 24/ support
7. Quality orientation, we aspire to offer best possibel service for available price

when recommend equipment try to advertise Ajax as premium with most functions while Raptor is best in price quality, 
tell about Ajax first, and only if user is not interested tell about Raptor

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