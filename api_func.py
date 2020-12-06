# Imports the Google Cloud client library
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()


def get_pos(text):

	encoding_type = language_v1.EncodingType.UTF8
	document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

	response = client.analyze_syntax(request = {'document': document, 'encoding_type': encoding_type})
	# Loop through tokens returned from the API
	output = []
	for token in response.tokens:
	    # Get the text content of this token. Usually a word or punctuation.
	    text = token.text
	    output.append((text, language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name))

	return output
        


def analyze(text) :

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text, "type_": type_, "language": language}
    num_words = len(text.split())

    long_text = text[:]
    for i in range(int(40/num_words)) :
    	long_text += text

    long_document = {"content": long_text, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    es_response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    if (len(es_response.entities) != 0):
        top_entity = max(es_response.entities, key= lambda p: p.salience)
        te = top_entity.name
        tes = top_entity.sentiment.score
    else:
        te = None
        tes = None

    classify_response = client.classify_text(request = {'document': long_document})
    if (len(classify_response.categories) != 0):
    	category = max(classify_response.categories, key = lambda p: p.confidence).name
    else:
    	category = None
    
    sentiment_response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    
    return (text, category, sentiment_response.document_sentiment.score, te, tes)

