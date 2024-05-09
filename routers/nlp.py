import spacy


def get_purpose_of_the_sentence(sentence):
    # Gets full sentence and returns the purpose mentioned in sentence
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    # Input sentence
    # sentence = "The modification consists in modifying harnesses installation for OHSC in Door Zone D3 LH FWD"

    # Process the sentence
    doc = nlp(sentence)

    # Extract the purpose (verb and object)
    purpose = ""
    for token in doc:
        #print(token, token.dep_, token.pos_)
        # if (token.dep_ == "nsubj" and token.pos_ == "NOUN") or (
        #         token.dep_ == "pcomp" and token.pos_ == "VERB"):
        if token.pos_ == "VERB":
            purpose += " " + token.text
            for child in token.children:
                #print("cccc = ", child, child.dep_, child.text)
                if child.dep_ == "dobj":
                    purpose += " " + child.text
                    break

    #print("Purpose:", purpose)
    return purpose


def extract_intention_v1(sentence):
    # Process the sentence using spaCy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    # Find the main verb (root)
    root = None
    for token in doc:
        if token.dep_ == "ROOT":
            root = token
            break

    # Initialize a list to store tokens representing the intention or outcome
    intention_tokens = []

    # Traverse the dependency tree to find tokens related to the main verb
    if root:
        for child in root.children:
            # Include tokens that modify the main verb or contribute to its action
            if child.dep_ in ("nsubj", "dobj", "attr", "advcl", "prep"):
                intention_tokens.append(child.text)

    # Return the extracted intention as a string
    return ' '.join(intention_tokens)


def extract_intention_v2(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    # Extract the main verb and direct object
    main_verb = None
    direct_object = None
    for token in doc:
        if token.dep_ == "ROOT":
            main_verb = token.text
        if token.dep_ == "dobj":
            direct_object = token.text

    # Construct the full sentence representing the intention or outcome
    if main_verb and direct_object:
        full_sentence = f"The intention is to {main_verb} {direct_object}."
        print(full_sentence)
    else:
        print("Unable to extract intention or outcome from the sentence.")
