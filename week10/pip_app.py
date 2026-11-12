"""Streamlit talking handbook: Pip transport/Kokoro, related rows, Qdrant evidence."""
from pathlib import Path
import json
import streamlit as st

from agent import Bot
from handbook import VectorIndex
from models import Conversation, Store, User
from pip_adapter import PipModel, local_reply
from qdrant_index import QdrantIndex

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Pip | Talking handbook')
st.title('Pip: a handbook, a memory and a voice')
st.caption('Fictional local profiles; answers cite the indexed PDF. Check every policy claim.')
base = st.sidebar.text_input('LM Studio URL', local_reply.DEFAULT_URL)
model = st.sidebar.text_input('Exact loaded model ID')
qdrant_port = st.sidebar.number_input('Qdrant port', min_value=1, max_value=65535, value=6333, step=1)
profile = st.sidebar.text_input('Fictional profile', 'Ada').strip()
chat_id = st.sidebar.number_input('Conversation ID (0 creates a new one)', min_value=0, step=1)
speak = st.sidebar.checkbox('Kokoro speech (Week 6 prepared assets)', value=True)
handbook = st.sidebar.selectbox('Handbook', ['Full PDF', 'Six-passage teaching fixture'])
bundle = ROOT / ('out/handbook-full.json' if handbook == 'Full PDF' else 'fixtures/handbook.json')

@st.cache_resource
def encoder(identity):
    from encoder import Encoder
    return Encoder(identity=identity)

@st.cache_resource
def voice():
    from synthesise_onnx import load_voice
    return load_voice('cpu')

if question := st.chat_input('Ask a short handbook question'):
    store = None
    try:
        if not profile or len(profile) > 80:
            raise ValueError('Use a fictional profile of 1-80 characters.')
        if not bundle.is_file():
            raise ValueError('Prepare the full PDF with qdrant_add_pdf.py first, '
                             'or select the six-passage teaching fixture.')
        index = VectorIndex.load(bundle)
        remote = QdrantIndex(index, port=qdrant_port)
        enc = encoder(index.encoder)
        if enc.identity != index.encoder:
            raise ValueError('Encoder differs; rebuild and reseed together.')
        model_client = PipModel(model, base)
        model_client.identity()
        store = Store(ROOT / 'out/pip.sqlite')
        user, _ = User.get_or_create(name=profile)
        key = (profile, int(chat_id))
        if chat_id:
            chat = store.owned_conversation(user.id, int(chat_id))
        else:
            if st.session_state.get('profile_key') != key:
                st.session_state['active_chat'] = Conversation.create(owner=user, title='Pip handbook').id
                st.session_state['profile_key'] = key
            chat = store.owned_conversation(user.id, st.session_state['active_chat'])
        st.info(f'Conversation {chat.id}. Reopen this ID after restarting the app. '
                f'{len(index.chunks)} indexed PDF passages; encoder: {index.encoder["name"]}.')
        for message in store.history(user.id, chat.id):
            with st.chat_message(message['role']):
                st.write(message['content'])
        with st.chat_message('user'):
            st.write(question)
        def retrieve(query):
            return remote.search_vector(enc.encode([query], query=True)[0], enc.identity)
        result = Bot(store, model_client, retrieve).ask(user.id, chat.id, question)
        with st.chat_message('assistant'):
            st.write(result['answer'])
        with st.expander('Inspect actual history, tool query and source evidence'):
            st.json(result)
        (ROOT / 'out/pip-last-turn.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        if speak:
            try:
                from synthesise_onnx import synthesise_reply
                data, seconds = synthesise_reply(result['answer'], device='cpu', voice=voice())
                st.audio(data, format='audio/wav', autoplay=True)
                st.caption(f'{seconds:.1f}s synthesized. Listen and check room volume; autoplay may need a click.')
            except Exception as error:
                st.error(f'Speech unavailable: {error}. The displayed turn remains saved.')
    except (OSError, RuntimeError, ValueError, KeyError, IndexError, TypeError) as error:
        st.error(f'Check setup and retry: {error}')
    finally:
        if store:
            store.close()
