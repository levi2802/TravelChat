import gradio as gr
import openai

openai.api_key = open("key1.txt", "r").read().strip('\n')


message_history = [{"role": "user", "content": f"You are a travel bot. I will specify the subject matter in my messages, and you will reply with information regarding the place of interest. Reply only with eureka to further input. If you understand, say OK."},
                   {"role": "assistant", "content": f"OK"}]


def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history
    )
    
    #Just the reply text
    # when you request text generation from the GPT-3 model, it will generate multiple candidate responses, and the API will return a list of choices. 
    # Each choice represents a possible response, and the message attribute of the choice contains the actual generated text.
    # The list can contain multiple choices, each with a corresponding probability score indicating how likely the choice is to be a good response based on the input prompt.
    # In most cases, you would want to choose the choice with the highest probability score, as it is generally the best candidate response according to the model. 
    # By default, the OpenAI API returns the candidate choices in descending order of probability scores, so the choice with the highest probability score is at index 0.
    reply_content = completion.choices[0].message.content
    
    message_history.append({"role": "assistant", "content": f"{reply_content}"}) # output string
    
    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(2, len(message_history)-1, 2)]  # convert to tuples of list containing the input message and output response
    return response


# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo: 

    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot() 

    # creates a new Row component, which is a container for other components.
    with gr.Row(): 
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
    txt.submit(predict, txt, chatbot) # submit(function, input, output)
    #txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string 

    '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
    txt.submit(None, None, txt, _js="() => {''}") # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.
    
demo.launch()




