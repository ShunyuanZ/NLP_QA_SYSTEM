# NLP_QA_SYSTEM

4.6-4.10

  Use Stanford NLP to parse a given document. Question generation functions, for each given tokenized     sentence, output the following questions:
    Type I: who-when-what-where
    Type II: yes/no

  Next, will do:
    1. Generated questions contain strings that are grammatical. So will need to use parser (e.g., PCFG     parser) to filter out those grammatical questions (with low probability)

    2. Add variance in generated questions, for example, use synonymy/antonym/hypernym/hypnoym.

    3. Add two more types of questions: how/why


2.26 - 3.3

  Questions: Preprocess Sample Code and Text Parsing Understanding.
  
    Question Generation Input: Text
    
    Question Generation Output: Questions, Text Parsing Tree.
  
  Answers: Retrieval Sample Code and Questions Parsing Sample Code and Test.
  
    Question Answering Input: Questions, Text Parsing Tree.
    
    Question Answering Output: Answers
    
# To be continued
