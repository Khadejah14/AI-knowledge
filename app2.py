# import streamlit as st
# import os
# import pdfplumber
# import docx2txt
# import chromadb
# from langchain.schema import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
# from openai import OpenAI
# import flashcards
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize clients
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# chroma_client = chromadb.PersistentClient(path="./knowledge_db")
# collection = chroma_client.get_or_create_collection(name="my_collection")

# # Initialize flashcard system
# flashcard_system = flashcards.FlashcardSystem()

# st.title("AI Coach Knowledge")
# st.write("Welcome to your AI coach, which is gonna help you in your learning journey")

# tab1, tab2, tab3 = st.tabs(["Upload & Process", "Study Flashcards", "Statistics & Settings"])

# with tab1:
#     file = st.file_uploader("Upload articles, notes, or past writings", type=['txt', "pdf", "docx"])
    
#     # Add a button to trigger processing
#     process_button = st.button("Generate Flashcards", type="primary", disabled=file is None)
    
#     if file is not None and process_button:
#         def extract_text_from_file(file):
#             if file.type == "application/pdf":
#                 text = ""
#                 with pdfplumber.open(file) as pdf:
#                     for page in pdf.pages:
#                         text += page.extract_text() + "\n"
#                 return text
#             elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#                 text = docx2txt.process(file)
#                 return text
#             elif file.type == "text/plain":
#                 text = file.read().decode("utf-8")
#                 return text
#             else:
#                 return None

#         def split_and_store_text(text):
#             headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
#             markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
#             header_chunks = markdown_splitter.split_text(text)

#             final_chunks = []
#             child_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=400,
#                 chunk_overlap=50,
#                 separators=["\n\n", "\n", "(?<=\. )", " ", ""]
#             )
            
#             for header_chunk in header_chunks:
#                 if len(header_chunk.page_content) < 500:
#                     final_chunks.append(header_chunk)
#                 else:
#                     sub_chunks = child_splitter.split_text(header_chunk.page_content)
#                     for sub_chunk in sub_chunks:
#                         new_chunk = Document(
#                             page_content=sub_chunk,
#                             metadata=header_chunk.metadata.copy()
#                         )
#                         final_chunks.append(new_chunk)
            
#             return final_chunks

#         def get_embedding(text):
#             response = client.embeddings.create(
#                 model="text-embedding-3-small",
#                 input=text
#             )
#             return response.data[0].embedding

#         def generate_qa_pairs(text_chunks):
#             all_qa_pairs = []
            
#             progress_bar = st.progress(0)
#             status_text = st.empty()
            
#             for i, chunk in enumerate(text_chunks):
#                 status_text.text(f"Processing chunk {i+1}/{len(text_chunks)}...")
#                 progress_bar.progress((i + 1) / len(text_chunks))
                
#                 sys_message = "You are a helpful tutor. Create exactly one clear question and a concise, factual answer based ONLY on the following text. The answer must be a single sentence found directly in the text. Format your response as: Q: [question] A: [answer]"
#                 user_prompt = f"Text: {chunk.page_content}"
                
#                 try:
#                     response = client.chat.completions.create(
#                         model="gpt-4o-mini",
#                         messages=[
#                             {"role": "system", "content": sys_message},
#                             {"role": "user", "content": user_prompt}
#                         ]
#                     )
                    
#                     generated_text = response.choices[0].message.content
                    
#                     # Parse the response to extract Q and A
#                     lines = generated_text.split('\n')
#                     question = None
#                     answer = None
                    
#                     for line in lines:
#                         if line.startswith('Q:'):
#                             question = line[2:].strip()
#                         elif line.startswith('A:'):
#                             answer = line[2:].strip()
                    
#                     if question and answer:
#                         source = f"{chunk.metadata.get('Header 1', '')} {chunk.metadata.get('Header 2', '')}".strip()
#                         all_qa_pairs.append({
#                             'question': question,
#                             'answer': answer,
#                             'context': chunk.page_content,
#                             'source': source or f"Chunk {i+1}"
#                         })
                        
#                 except Exception as e:
#                     st.error(f"Error generating Q&A for chunk {i+1}: {str(e)}")
            
#             progress_bar.empty()
#             status_text.empty()
#             return all_qa_pairs

#         def store_in_vector_db(text_chunks, qa_pairs):
#             ids = []
#             documents = []
#             embeddings = []
#             metadatas = []
            
#             for i, (chunk, qa_pair) in enumerate(zip(text_chunks, qa_pairs)):
#                 embedding = get_embedding(chunk.page_content)
#                 ids.append(f"chunk_{i}")
#                 documents.append(chunk.page_content)
#                 embeddings.append(embedding)
#                 metadatas.append({
#                     "header": f"{chunk.metadata.get('Header 1', '')} {chunk.metadata.get('Header 2', '')}".strip(),
#                     "question": qa_pair['question'],
#                     "answer": qa_pair['answer']
#                 })
            
#             # Add all at once to ChromaDB
#             collection.add(
#                 ids=ids,
#                 documents=documents,
#                 embeddings=embeddings,
#                 metadatas=metadatas
#             )

#         # Main processing logic
#         text = extract_text_from_file(file)
#         if text:
#             with st.spinner("Processing your document..."):
#                 chunks = split_and_store_text(text)
                
#                 # Generate Q&A pairs
#                 qa_pairs = generate_qa_pairs(chunks)
                
#                 if qa_pairs:
#                     # Store in vector database
#                     store_in_vector_db(chunks, qa_pairs)
                    
#                     # Add to flashcard system
#                     flashcard_system.add_flashcards(qa_pairs)
                    
#                     st.success(f"Processed {len(chunks)} text chunks and created {len(qa_pairs)} flashcards!")
#                     st.info("Switch to the 'Study Flashcards' tab to start learning!")
                    
#                     # Show sample of generated flashcards
#                     with st.expander("View sample flashcards"):
#                         for i, pair in enumerate(qa_pairs[:3]):  # Show first 3
#                             st.write(f"**Q:** {pair['question']}")
#                             st.write(f"**A:** {pair['answer']}")
#                             st.write("---")
#                 else:
#                     st.error("Failed to generate any flashcards from the document.")
#     elif file is None and process_button:
#         st.warning("Please upload a file first!")

# # with tab2:
# #     st.header("Study Flashcards")
# #     flashcard_system.display_flashcard_interface()

# # with tab3:
# #     st.header("Statistics & Settings")
# #     flashcard_system.display_stats_dashboard()
    
# #     # Display all flashcards for review
# #     if hasattr(flashcard_system, 'flashcards') and flashcard_system.flashcards:
# #         st.subheader("All Flashcards")
# #         for i, card in enumerate(flashcard_system.flashcards):
# #             with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
# #                 st.write(f"**Question:** {card['question']}")
# #                 st.write(f"**Answer:** {card['answer']}")
# #                 if card.get('context'):
# #                     st.write(f"**Context:** {card['context']}")
# #                 if card.get('source'):
# #                     st.write(f"**Source:** {card['source']}")
                
# #                 # Show statistics for this card
# #                 if hasattr(flashcard_system, 'card_stats') and card['id'] in flashcard_system.card_stats:
# #                     stats = flashcard_system.card_stats[card['id']]
# #                     total_attempts = stats['views']
# #                     if total_attempts > 0:
# #                         accuracy = stats['correct'] / total_attempts * 100
# #                         st.write(f"**Stats:** {total_attempts} reviews, {accuracy:.1f}% accuracy")
# with tab2:
#     st.header("Study Flashcards")
#     flashcard_system.display_flashcard_interface()

# with tab3:
#     st.header("Statistics & Settings")
#     flashcard_system.display_stats_dashboard()
    
#     # Display all flashcards for review
#     if flashcard_system.flashcards:
#         st.subheader("All Flashcards")
#         for i, card in enumerate(flashcard_system.flashcards):
#             with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
#                 st.write(f"**Question:** {card['question']}")
#                 st.write(f"**Answer:** {card['answer']}")
#                 if card.get('context'):
#                     st.write(f"**Context:** {card['context']}")
#                 if card.get('source'):
#                     st.write(f"**Source:** {card['source']}")
                
#                 # Show statistics for this card
#                 card_stats = flashcard_system.card_stats
#                 if card['id'] in card_stats:
#                     stats = card_stats[card['id']]
#                     total_attempts = stats['views']
#                     if total_attempts > 0:
#                         accuracy = stats['correct'] / total_attempts * 100
#                         st.write(f"**Stats:** {total_attempts} reviews, {accuracy:.1f}% accuracy")
#                     else:
#                         st.write("**Stats:** No reviews yet")
#########################################################################3
import streamlit as st
import os

import docx2txt
import chromadb
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from openai import OpenAI
import flashcards
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./knowledge_db")
collection = chroma_client.get_or_create_collection(name="my_collection")

# Initialize flashcard system with demo flashcards
flashcard_system = flashcards.FlashcardSystem()

# Add some demo flashcards if none exist
if not flashcard_system.flashcards:
    demo_flashcards = [
        {
            'question': 'What is the capital of France?',
            'answer': 'Paris',
            'context': 'Geography and European capitals',
            'source': 'Demo Content'
        },
        {
            'question': 'What is the largest planet in our solar system?',
            'answer': 'Jupiter',
            'context': 'Astronomy and planetary science',
            'source': 'Demo Content'
        },
        {
            'question': 'Who wrote "Romeo and Juliet"?',
            'answer': 'William Shakespeare',
            'context': 'English literature and playwrights',
            'source': 'Demo Content'
        }
    ]
    flashcard_system.add_flashcards(demo_flashcards)

st.title("AI Coach Knowledge")
st.write("Welcome to your AI coach, which is gonna help you in your learning journey")
st.write("this is a demo version with sample flashcards to see how it works, cuz uploading and processing is gonna finish my tokens ")

tab1, tab2, tab3 = st.tabs(["Upload & Process", "Study Flashcards", "Statistics & Settings"])

with tab1:
    file = st.file_uploader("Upload articles, notes, or past writings", type=['txt', "pdf", "docx"])
    
    # Add a button to trigger processing
    # process_button = st.button("Generate Flashcards", type="primary", disabled=file is None)
    
    # if file is not None and process_button:
    #     def extract_text_from_file(file):
    #         if file.type == "application/pdf":
    #             text = ""
    #             with pdfplumber.open(file) as pdf:
    #                 for page in pdf.pages:
    #                     text += page.extract_text() + "\n"
    #             return text
    #         elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    #             text = docx2txt.process(file)
    #             return text
    #         elif file.type == "text/plain":
    #             text = file.read().decode("utf-8")
    #             return text
    #         else:
    #             return None

    #     def split_and_store_text(text):
    #         headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
    #         markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)
    #         header_chunks = markdown_splitter.split_text(text)

    #         final_chunks = []
    #         child_splitter = RecursiveCharacterTextSplitter(
    #             chunk_size=400,
    #             chunk_overlap=50,
    #             separators=["\n\n", "\n", "(?<=\. )", " ", ""]
    #         )
            
    #         for header_chunk in header_chunks:
    #             if len(header_chunk.page_content) < 500:
    #                 final_chunks.append(header_chunk)
    #             else:
    #                 sub_chunks = child_splitter.split_text(header_chunk.page_content)
    #                 for sub_chunk in sub_chunks:
    #                     new_chunk = Document(
    #                         page_content=sub_chunk,
    #                         metadata=header_chunk.metadata.copy()
    #                     )
    #                     final_chunks.append(new_chunk)
            
    #         return final_chunks

    #     def get_embedding(text):
    #         response = client.embeddings.create(
    #             model="text-embedding-3-small",
    #             input=text
    #         )
    #         return response.data[0].embedding

    #     def generate_qa_pairs(text_chunks):
    #         all_qa_pairs = []
            
    #         progress_bar = st.progress(0)
    #         status_text = st.empty()
            
    #         for i, chunk in enumerate(text_chunks):
    #             status_text.text(f"Processing chunk {i+1}/{len(text_chunks)}...")
    #             progress_bar.progress((i + 1) / len(text_chunks))
                
    #             sys_message = "You are a helpful tutor. Create exactly one clear question and a concise, factual answer based ONLY on the following text. The answer must be a single sentence found directly in the text. Format your response as: Q: [question] A: [answer]"
    #             user_prompt = f"Text: {chunk.page_content}"
                
    #             try:
    #                 response = client.chat.completions.create(
    #                     model="gpt-4o-mini",
    #                     messages=[
    #                         {"role": "system", "content": sys_message},
    #                         {"role": "user", "content": user_prompt}
    #                     ]
    #                 )
                    
    #                 generated_text = response.choices[0].message.content
                    
    #                 # Parse the response to extract Q and A
    #                 lines = generated_text.split('\n')
    #                 question = None
    #                 answer = None
                    
    #                 for line in lines:
    #                     if line.startswith('Q:'):
    #                         question = line[2:].strip()
    #                     elif line.startswith('A:'):
    #                         answer = line[2:].strip()
                    
    #                 if question and answer:
    #                     source = f"{chunk.metadata.get('Header 1', '')} {chunk.metadata.get('Header 2', '')}".strip()
    #                     all_qa_pairs.append({
    #                         'question': question,
    #                         'answer': answer,
    #                         'context': chunk.page_content,
    #                         'source': source or f"Chunk {i+1}"
    #                     })
                        
    #             except Exception as e:
    #                 st.error(f"Error generating Q&A for chunk {i+1}: {str(e)}")
            
    #         progress_bar.empty()
    #         status_text.empty()
    #         return all_qa_pairs

    #     def store_in_vector_db(text_chunks, qa_pairs):
    #         ids = []
    #         documents = []
    #         embeddings = []
    #         metadatas = []
            
    #         for i, (chunk, qa_pair) in enumerate(zip(text_chunks, qa_pairs)):
    #             embedding = get_embedding(chunk.page_content)
    #             ids.append(f"chunk_{i}")
    #             documents.append(chunk.page_content)
    #             embeddings.append(embedding)
    #             metadatas.append({
    #                 "header": f"{chunk.metadata.get('Header 1', '')} {chunk.metadata.get('Header 2', '')}".strip(),
    #                 "question": qa_pair['question'],
    #                 "answer": qa_pair['answer']
    #             })
            
    #         # Add all at once to ChromaDB
    #         collection.add(
    #             ids=ids,
    #             documents=documents,
    #             embeddings=embeddings,
    #             metadatas=metadatas
    #         )

    #     # Main processing logic
    #     text = extract_text_from_file(file)
    #     if text:
    #         with st.spinner("Processing your document..."):
    #             chunks = split_and_store_text(text)
                
    #             # Generate Q&A pairs
    #             qa_pairs = generate_qa_pairs(chunks)
                
    #             if qa_pairs:
    #                 # Store in vector database
    #                 store_in_vector_db(chunks, qa_pairs)
                    
    #                 # Add to flashcard system
    #                 flashcard_system.add_flashcards(qa_pairs)
                    
    #                 st.success(f"Processed {len(chunks)} text chunks and created {len(qa_pairs)} flashcards!")
    #                 st.info("Switch to the 'Study Flashcards' tab to start learning!")
                    
    #                 # Show sample of generated flashcards
    #                 with st.expander("View sample flashcards"):
    #                     for i, pair in enumerate(qa_pairs[:3]):  # Show first 3
    #                         st.write(f"**Q:** {pair['question']}")
    #                         st.write(f"**A:** {pair['answer']}")
    #                         st.write("---")
    #             else:
    #                 st.error("Failed to generate any flashcards from the document.")
    # elif file is None and process_button:
    #     st.warning("Please upload a file first!")

with tab2:
    st.header("Study Flashcards")
    flashcard_system.display_flashcard_interface()

with tab3:
    st.header("Statistics & Settings")
    flashcard_system.display_stats_dashboard()
    
    # Display all flashcards for review
    if flashcard_system.flashcards:
        st.subheader("All Flashcards")
        for i, card in enumerate(flashcard_system.flashcards):
            with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
                st.write(f"**Question:** {card['question']}")
                st.write(f"**Answer:** {card['answer']}")
                if card.get('context'):
                    st.write(f"**Context:** {card['context']}")
                if card.get('source'):
                    st.write(f"**Source:** {card['source']}")
                
                # Show statistics for this card
                card_stats = flashcard_system.card_stats
                if card['id'] in card_stats:
                    stats = card_stats[card['id']]
                    total_attempts = stats['views']
                    if total_attempts > 0:
                        accuracy = stats['correct'] / total_attempts * 100
                        st.write(f"**Stats:** {total_attempts} reviews, {accuracy:.1f}% accuracy")
                    else:

                        st.write("**Stats:** No reviews yet")
