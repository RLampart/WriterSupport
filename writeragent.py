import language_tool_python

class GrammarCheckingAgent:
    def __init__(self, language='en-UK'):
        self.tool = language_tool_python.LanguageToolPublicAPI(language)

    def check_grammar(self, text):
        matches = self.tool.check(text)
        return matches

    def correct_grammar(self, text):
        corrected_text = self.tool.correct(text)
        return corrected_text

    def run(self, text):
        print("Original Text:")
        print(text)
        print("\nChecking for grammatical errors...\n")
        
        matches = self.check_grammar(text)
        if matches:
            print("Found the following issues:")
            for match in matches:
                print(f" - {match.message}")
                print(f"   Suggestion: {match.replacements}")
                print(f"   Context: {match.context}")
                print()
            
            corrected_text = self.correct_grammar(text)
            print("Corrected Text:")
            print(corrected_text)
        else:
            print("No grammatical errors found.")
            corrected_text = text
        
        return corrected_text

if __name__ == "__main__":
    text = "This is an example sentence with a grammatical mistake. She go to the store yesterday."
    agent = GrammarCheckingAgent()
    corrected_text = agent.run(text)
    print("\nFinal Corrected Text:")
    print(corrected_text)
