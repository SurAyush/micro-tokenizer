import wikipedia

query = "Taylor Swift"  # Intentionally misspelled to test correction

# Try to get a better match
suggested_title = wikipedia.suggest(query)

# If there's a suggestion, use it; otherwise, search for matches
page_title = suggested_title if suggested_title else query

try:
    page = wikipedia.page(page_title, auto_suggest=True)
    print(f"Extracting from: {page.title}")

    # Save content to a text file
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(page.content)

    print("Text extracted and saved to output.txt")

except wikipedia.exceptions.PageError:
    print("Error: The page does not exist. Try refining your search.")

except wikipedia.exceptions.DisambiguationError as e:
    print("Error: The query is ambiguous. Try one of these options:")
    print(e.options)  # Print suggested options