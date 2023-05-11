import streamlit as st


from streamlit_chat import message
from googletrans import Translator
from audio_recorder_streamlit import audio_recorder
import io
from PIL import Image

from predict import *

st.set_page_config(page_title="IU Tư Vấn Tuyển Sinh (IU Admissions Consultant)", layout = 'centered')


iulogo = Image.open('IUlogo.png')
vnulogo = Image.open('VNUlogo.png')

colx, coly= st.columns([1,1])
with colx:
    st.image(iulogo, caption='',  width=150)
with coly:
    st.image(vnulogo, caption='',  width=400)

    

st.title("ĐẠI HỌC QUỐC TẾ - ĐHQG TPHCM")
st.markdown("**INTERNATIONAL UNIVERSITY - VIETNAM NATIONAL UNIVERSITY HCM CITY**")

st.header('🤖CHATBOT')

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
    
user_input = st.text_input("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖","", placeholder = "Nhập tin nhắn (Typing here)...", help = "Vui lòng nhập đúng chính tả(Please enter correct spelling)",key="text")
text = ''                

       
st.sidebar.selectbox("Câu hỏi gợi ý (Example questions)",list(df["Question"]))

def clear_text():
    st.session_state["text"] = ""
    text = ''                


col1, col2, col3, col4, col5 = st.columns([0.24,0.2,0.2,0.2,1])
with col1:
    with st.form(key='my_form', clear_on_submit=True):
        submit_button = st.form_submit_button(label='▶️', help = "Gửi (Send)")
with col2:
    st.button("↩️", on_click=clear_text, help = "Xóa tin nhắn (Clear input)")

with col3:
    if st.button("🗑️",help = 'Xóa đoạn chat/Xóa ngữ cảnh (Clear context)', on_click=clear_text):
        text = ''                
        st.session_state['past'] = []
        st.session_state['generated'] = []
        st.experimental_rerun()

# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):        
#     if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:           
#         print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        
with col4:
    audio_data = audio_recorder(text="", icon_size="2x") 


with col5:
    st.button("🖇️🏞️",help = "🖇️Chèn ảnh (Insert Image)")
    
    
st.markdown('_Nếu câu trả lời không hợp lý, vui lòng tải lại trang (If the answer not make sense, please reload the page)_')
    
st.markdown('----')
    
if audio_data:
    # st.audio(audio_data, format='audio/wav')
    with io.BytesIO(audio_data) as audio_file:
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio_file.read())

    r = sr.Recognizer()

    with sr.AudioFile("recorded_audio.wav") as source:
        audio_text = r.record(source)
    try:
        text = r.recognize_google(audio_text, language = 'vi-VI', show_all = True)
        # st.session_state.past.append(text['alternative'][0]['transcript'])
        # st.write(text['alternative'][0]['transcript'])
        text = text['alternative'][0]['transcript']
        text = text.lower()
    except:
        st.write(":red[_Vui lòng ghi âm lại, sau khi bấm nút hãy chờ 2 giây trước khi nói (Please record again, after pressing the button wait 2 seconds before speaking)_]")    


if user_input:
  text = ''                
  if re.search(r"(chỉ tiêu)|(giới thiệu)|(cho tôi hỏi)|(là gì)", user_input.lower()):
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + user_input
    else:
        inp = user_input


    inp = re.sub(r"(chào)|(hello)|(hi)|(xin chào)|(điểm chuẩn)|(học những môn nào)|(có những môn nào)|(có học)|(học những môn gì)|(học môn nào)|(học môn gì)|(học những môn chính gì)|(khối)","",inp)
    output = chat_bot(inp)


    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)


  elif re.search(r"(chào)|(hello)|(hi)|(xin chào)|(điểm chuẩn)", user_input):
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + user_input
    else:
        inp = user_input
    output = chat_bot(inp)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    
  elif re.search(r"tổ hợp xét tuyển", user_input.lower()):
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + user_input
    else:
        inp = user_input
    inp = re.sub(r"(chào)|(hello)|(hi)|(xin chào)|(điểm chuẩn)|(chỉ tiêu)|(học những môn nào)|(có những môn nào)|(có học)|(học những môn gì)|(học môn nào)|(học môn gì)|(học những môn chính gì)|(khối)","",inp)
    output = chat_bot(inp)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    
  else:
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + user_input
    else:
        inp = user_input
    inp = re.sub(r"(chào)|(hello)|(hi)|(xin chào)","",inp)

    output = chat_bot(inp)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)
    

if text:
  if re.search(r"(chỉ tiêu)|(giới thiệu)|(cho tôi hỏi)|(là gì)", text.lower()):
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + text
    else:
        inp = text


    inp = re.sub(r"(chào)|(hello)|(hi)|(xin chào)|(điểm chuẩn)|(học những môn nào)|(có những môn nào)|(có học)|(học những môn gì)|(học môn nào)|(học môn gì)|(học những môn chính gì)|(khối)","",inp)
    output = chat_bot(inp)


    st.session_state.past.append(text)
    st.session_state.generated.append(output)


  elif re.search(r"(chào)|(hello)|(hi)|(xin chào)|(điểm chuẩn)", text.lower()):
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + text
    else:
        inp = text
    output = chat_bot(inp)
    st.session_state.past.append(text)
    st.session_state.generated.append(output)
  elif re.search(r"tổ hợp xét tuyển", text.lower()):
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + text
    else:
        inp = text
    inp = re.sub(r"(chào)|(hello)|(hi)|(xin chào)|(điểm chuẩn)|(chỉ tiêu)|(học những môn nào)|(có những môn nào)|(có học)|(học những môn gì)|(học môn nào)|(học môn gì)|(học những môn chính gì)|(khối)","",inp)
    output = chat_bot(inp)
    st.session_state.past.append(text)
    st.session_state.generated.append(output)
        
    
  else:
    if st.session_state['past'] != []:
        inp =  ' '.join(tokenize_input(' '.join(st.session_state['past'][-3:])))  + ' ' + text
    else:
        inp = text
    inp = re.sub(r"(chào)|(hello)|(hi)|(xin chào)","",inp)

    output = chat_bot(inp)
    st.session_state.past.append(text)
    st.session_state.generated.append(output)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')



st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')
st.markdown(' ')

st.markdown('➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖')
st.markdown('@Copyright: **Ly Minh Trung** 🇻🇳')
st.markdown('Beta Version')
                