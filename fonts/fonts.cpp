// Set up font for text
sf::Font font;
if (!font.loadFromFile("../../fonts/Arialn.ttf")) {
    cerr << "Error loading font file." << endl;
    return EXIT_FAILURE;
}