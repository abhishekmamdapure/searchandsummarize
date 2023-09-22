import openai
import time 

def GPTValidator(sys_PROMPT='',usr_PROMPT='', model = "gpt-3.5-turbo",OPENAI_API_KEY=''):   
    
    if not OPENAI_API_KEY:     
        print('Enter OPENAI_API_KEY in sidebar')
    else:
        openai.api_key = OPENAI_API_KEY

    try:

        completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_PROMPT},
            {"role": "user", "content": usr_PROMPT}]
            )

        return completion.choices[0].message['content']
    
    except openai.error.RateLimitError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_PROMPT},
            {"role": "user", "content": usr_PROMPT}]
            )
        return completion.choices[0].message['content']
    
    except openai.error.APIError as e:
        retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
        print(f"API error occurred. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_PROMPT},
            {"role": "user", "content": usr_PROMPT}]
            )
        return completion.choices[0].message['content']

    except OSError as e:
        retry_time = 5  # Adjust the retry time as needed
        print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")      
        time.sleep(retry_time)
        completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_PROMPT},
            {"role": "user", "content": usr_PROMPT}]
            )
        return completion.choices[0].message['content']
    
    except openai.error.ServiceUnavailableError as e:
        retry_time = 10  # Adjust the retry time as needed
        print(f"Service unavailable error occurred: {e}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": sys_PROMPT},
            {"role": "user", "content": usr_PROMPT}]
            )
        return completion.choices[0].message['content']