from shiny import App, Inputs, Outputs, Session, render, ui
import json

# Define the list of items for auto-suggest
item_list = ["apple", "banana", "grape", "orange", "pear", "peach", "plum", "kiwi"]

app_ui = ui.page_fluid(
    ui.input_text("search_box", "Type to search", ""),
    ui.div(id="selected_items", style="margin-top: 20px; padding: 10px; display: none;"),
    ui.tags.script(f"""
        document.addEventListener('DOMContentLoaded', function() {{
            var availableTags = {json.dumps(item_list)};
            var searchBox = document.getElementById('search_box');
            var selectedItemsDiv = document.getElementById('selected_items');

            searchBox.addEventListener('input', function(event) {{
                var value = event.target.value.trim();
                if (value === '') {{
                    selectedItemsDiv.innerHTML = '';
                    selectedItemsDiv.style.display = 'none';
                    return;
                }}
                
                var inputValues = value.split(',').map(function(item) {{ return item.trim(); }});
                var currentInput = inputValues[inputValues.length - 1].toLowerCase();

                var suggestions = availableTags.filter(function(tag) {{
                    return tag.toLowerCase().includes(currentInput) && !inputValues.includes(tag);
                }});
                showSuggestions(suggestions);
            }});

            function showSuggestions(suggestions) {{
                selectedItemsDiv.innerHTML = '';
                if (suggestions.length === 0) {{
                    selectedItemsDiv.style.display = 'none';
                    return;
                }}
                suggestions.forEach(function(suggestion) {{
                    var suggestionItem = document.createElement('div');
                    suggestionItem.textContent = suggestion;
                    suggestionItem.classList.add('suggestion-item');
                    suggestionItem.style.cursor = 'pointer';
                    suggestionItem.style.padding = '5px';
                    suggestionItem.style.borderBottom = '1px solid #ddd';
                    suggestionItem.addEventListener('click', function() {{
                        var inputValues = searchBox.value.split(',').map(function(item) {{ return item.trim(); }});
                        inputValues[inputValues.length - 1] = suggestion;
                        searchBox.value = inputValues.join(', ');
                        selectedItemsDiv.innerHTML = '';
                        selectedItemsDiv.style.display = 'none';
                    }});
                    suggestionItem.addEventListener('mouseenter', function() {{
                        suggestionItem.style.backgroundColor = 'blue';
                        suggestionItem.style.color = 'white';
                    }});
                    suggestionItem.addEventListener('mouseleave', function() {{
                        suggestionItem.style.backgroundColor = '';
                        suggestionItem.style.color = '';
                    }});
                    selectedItemsDiv.appendChild(suggestionItem);
                }});
                selectedItemsDiv.style.display = 'block';
            }}
        }});
    """)
)

def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.ui
    async def selected_items():
        selected_item = input.selected_item()
        if selected_item:
            # Append the selected item to the output box
            existing_items = session.user_data.get('selected_items', [])
            if selected_item not in existing_items:
                existing_items.append(selected_item)
            session.user_data['selected_items'] = existing_items
            # Generate the output UI
            return [ui.div(item) for item in existing_items]
        else:
            return ui.div("No items selected yet")

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
