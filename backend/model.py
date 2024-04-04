import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_is_in_danger(user_prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_prompt}],
        functions=[
            {
                "name": "get_danger_info",
                "description": "Get whether the person is in danger or not",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_danger": {
                            "type": "boolean",
                            "description": "The person is in danger. E.g. True, False",
                        }
                    },
                    "required": ["is_danger"],
                },
            }
        ],
        function_call={"name": "get_danger_info"},
    )

    output = completion.choices[0].message

    def get_danger_info(is_danger):
        """Get whether the person is in danger or not"""
        return is_danger

    origin = json.loads(output.function_call.arguments).get("is_danger")
    params = json.loads(output.function_call.arguments)
    type(params)
    chosen_function = eval(output.function_call.name)
    is_danger = chosen_function(**params)
    return is_danger
