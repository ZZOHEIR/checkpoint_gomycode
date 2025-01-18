import os
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK data
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

data_wiki = '''A member of the wealthy South African Musk family, Musk was born in Pretoria and briefly attended the University of Pretoria. At the age of 18 he immigrated to Canada, acquiring its citizenship through his Canadian-born mother, Maye. Two years later, he matriculated at Queen's University in Canada. Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but never enrolled in classes, and with his brother Kimbal co-founded the online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999. That same year, Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal. In 2002, Musk acquired United States citizenship, and that October eBay acquired PayPal for $1.5 billion. Using $100 million of the money he made from the sale of PayPal, Musk founded SpaceX, a spaceflight services company, in 2002.
In 2004, Musk was an early investor in electric-vehicle manufacturer Tesla Motors, Inc. (later Tesla, Inc.), providing most of the initial financing and assuming the position of the company's chairman. He later became the product architect and, in 2008, the CEO. In 2006, Musk helped create SolarCity, a solar energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, he proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year Musk co-founded Neuralink, a neurotechnology company developing brain–computer interfaces, and the Boring Company, a tunnel construction company. In 2018, the U.S. Securities and Exchange Commission (SEC) sued Musk, alleging he falsely announced that he had secured funding for a private takeover of Tesla. To settle the case, Musk stepped down as the chairman of Tesla and paid a $20 million fine. In 2022, he acquired Twitter for $44 billion, merged the company into his newly-created X Corp. and rebranded the service as X the following year. In 2023, Musk founded xAI, an artificial intelligence company.
'''



def preprocess(text):
    # Tokenize the text into words
    words = word_tokenize(text, language='english')
    # Convert to lower case
    words = [word.lower() for word in words]
    # Remove punctuation
    words = [word for word in words if word.isalpha()]
    # Define custom stop words
    custom_stop_words = set(stopwords.words('english')).union({"mrs", "mr", "said"})
    words = [word for word in words if word not in custom_stop_words]
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)  # Join words back into a single string




def most_relevant_sentence(query, processed_sentences):
    max_similarity = 0
    relevant_sentence = " "

    # Compute Jaccard similarity between the query and each sentence in the vocabulary
    for sentence in processed_sentences:
        intersection = set(query).intersection(sentence)
        union = set(query).union(sentence)
        similarity = len(intersection) / len(union)
        if similarity > max_similarity:
            max_similarity = similarity
            relevant_sentence = " ".join(sentence)
    return relevant_sentence

    

def chatbot(query, processed_sentences):
    relevant_sentence = most_relevant_sentence(query, processed_sentences)
    return relevant_sentence

def main():
    st.title("Chatbot Interface")
    st.write("Ask your question below:")

    user_query = st.text_input("Your Question:", "")
    
    if st.button("Submit"):
        if user_query:
            text = data_wiki
            print(user_query)


            sentences = sent_tokenize(text)
            processed_sentences = [preprocess(sentence) for sentence in sentences]
            response = chatbot(preprocess(user_query), processed_sentences)
            st.write("Chatbot Response:")
            st.write(response)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
