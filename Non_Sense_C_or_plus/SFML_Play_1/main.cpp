// g++ main.cpp -lsfml-graphics -lsfml-window -lsfml-system -o main

#include <SFML/Graphics.hpp>
#include <iostream>

int parse_bits_from_argv(char* bitString, int in_bits[4]) {
    int error = 1;
    int no_error = 0;

    for(int i = 0; bitString[i] != '\0'; ++i) {
        int casted_bit = (((int)bitString[i]) - 48);
        if (!(casted_bit == 0 || casted_bit == 1)) {
            std::cout << "Enter binary digits only (1,0)!" << '\n';
            return error;
        }
        in_bits[i] =  ((int)bitString[i]) - 48;
    }

    return no_error;
}

void xor_the_bits(int in_a[4], int in_b[4], int out[4]) {
    for(int i = 0; i < 4; ++i) {
        out[i] = in_a[i] ^ in_b[i];
    }
}

int main(int argc, char* argv[])
{
    int in_a_bits[4] = {0};
    int in_b_bits[4] = {0};
    int out_bits[4] = {0};

    if(argc < 3) {
        std::cout << "Enter two inputs (4-bits each)" << '\n';
        return 0x0;
    }

    int is_error = parse_bits_from_argv(argv[1], in_a_bits);
    if(is_error) {
        exit(1);
    }
    is_error = parse_bits_from_argv(argv[2], in_b_bits);
    if(is_error) {
        exit(1);
    }

    xor_the_bits(in_a_bits, in_b_bits, out_bits);

    sf::RenderWindow window(sf::VideoMode({500, 600}), "SFML works!");
    sf::RectangleShape rectangle({120.f, 50.f});

    sf::Font font;
    if (!font.loadFromFile("arial.ttf"))
    {
        std::cout << "Sad, no font file :3" << '\n';
    }

    rectangle.setSize({150.f, 325.f});
    rectangle.setPosition({180.f, 100.f});
    rectangle.setFillColor(sf::Color(100, 250, 50));

    sf::RectangleShape in_line_1({150.f, 5.f});
    sf::RectangleShape in_line_2({150.f, 5.f});
    sf::RectangleShape in_line_3({150.f, 5.f});
    sf::RectangleShape in_line_4({150.f, 5.f});

    sf::RectangleShape in_line_5({150.f, 5.f});
    sf::RectangleShape in_line_6({150.f, 5.f});
    sf::RectangleShape in_line_7({150.f, 5.f});
    sf::RectangleShape in_line_8({150.f, 5.f});

    sf::RectangleShape out_line_1({150.f, 5.f});
    sf::RectangleShape out_line_2({150.f, 5.f});
    sf::RectangleShape out_line_3({150.f, 5.f});
    sf::RectangleShape out_line_4({150.f, 5.f});

    in_line_1.setPosition({100.f, 100.f});
    in_line_2.setPosition({100.f, 140.f});
    in_line_3.setPosition({100.f, 180.f});
    in_line_4.setPosition({100.f, 220.f});

    in_line_5.setPosition({100.f, 300.f});
    in_line_6.setPosition({100.f, 340.f});
    in_line_7.setPosition({100.f, 380.f});
    in_line_8.setPosition({100.f, 420.f});

    out_line_1.setPosition({260.f, 200.f});
    out_line_2.setPosition({260.f, 240.f});
    out_line_3.setPosition({260.f, 280.f});
    out_line_4.setPosition({260.f, 320.f});

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();

        
        window.draw(in_line_1);
        window.draw(in_line_2);
        window.draw(in_line_3);
        window.draw(in_line_4);

        window.draw(in_line_5);
        window.draw(in_line_6);
        window.draw(in_line_7);
        window.draw(in_line_8);

        window.draw(out_line_1);
        window.draw(out_line_2);
        window.draw(out_line_3);
        window.draw(out_line_4);

        window.draw(rectangle);

        for(int i = 0; i < 4; i++) {
            sf::Text text;
            text.setFont(font);
            text.setString((char)(in_a_bits[i] + 48));
            text.setCharacterSize(24);
            text.setFillColor(sf::Color::Red);
            text.setPosition({80.f, 90.f + i * 40});
            window.draw(text);
        }

        for(int i = 0; i < 4; i++) {
            sf::Text text;
            text.setFont(font);
            text.setString((char)(in_b_bits[i] + 48));
            text.setCharacterSize(24);
            text.setFillColor(sf::Color::Red);
            text.setPosition({80.f, 290.f + i * 40});
            window.draw(text);
        }

        for(int i = 0; i < 4; i++) {
            sf::Text text;
            text.setFont(font);
            text.setString((char)(out_bits[i] + 48));
            text.setCharacterSize(24);
            text.setFillColor(sf::Color::Red);
            text.setPosition({420.f, 190.f + i * 40});
            window.draw(text);
        }

        window.display();
    }

    return 0;
}
