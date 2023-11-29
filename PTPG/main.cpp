#include <iostream>
#include <SFML/Graphics.hpp>

//using namespace std;

int main() {
    // Create a window with the title "SFML Window" and a size of 800x600 pixels
    sf::RenderWindow window(sf::VideoMode(800, 600), "SFML Window");

    // Use the default font that comes with SFML
    sf::Font font;
    font.loadFromFile("arial.ttf");
    /*
    if (!font.loadFromFile("arial.ttf")) {
        std::cerr << "Error loading font file." << std::endl;
        return EXIT_FAILURE;
    }
    */
    // Create text for the prompt
    sf::Text promptText("Are you sure you want to exit?", font, 20);
    promptText.setPosition(20.f, 50.f);

    // Create "Yes" and "No" buttons
    sf::Text yesText("Yes", font, 20);
    yesText.setPosition(120.f, 120.f);

    sf::Text noText("No", font, 20);
    noText.setPosition(260.f, 120.f);

    // Run the program as long as the window is open
    while (window.isOpen()) {

        // Check all the window's events that were triggered since the last iteration of the loop
        sf::Event event;
        while (window.pollEvent(event)) {

            // "Close requested" event: we show closing prompt
            if (event.type == sf::Event::Closed) {

                while (true) {
                    window.clear();
                    window.draw(promptText);
                    window.draw(yesText);
                    window.draw(noText);
                    window.display();

                    sf::Event promptEvent;
                    while (window.pollEvent(promptEvent)) {
                        if (promptEvent.type == sf::Event::Closed) {
                            // If the user closes the prompt, close the program
                            window.close();
                            break;
                        }
                        else if (promptEvent.type == sf::Event::MouseButtonPressed) {
                            // If the user clicks "Yes" or "No", handle accordingly
                            sf::Vector2f mousePos = window.mapPixelToCoords(sf::Mouse::getPosition(window));
                            if (yesText.getGlobalBounds().contains(mousePos)) {
                                window.close(); // Close the program
                            }
                            else if (noText.getGlobalBounds().contains(mousePos)) {
                                break; // Close the prompt and continue the main loop
                            }
                        }
                    }
                }
            }
        }
        
        // Clear the window with a black color
        window.clear(sf::Color::Black);\

        // Main window content    
        sf::Text mainText("Main Content", font, 20);
        mainText.setPosition(20.f, 100.f);
        window.draw(mainText);

        // Display what has been rendered to the window so far
        window.display();
    }

    return 0;
}
