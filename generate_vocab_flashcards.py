import genanki
import logging
from argparse import ArgumentParser


MODEL_ID = 1983249569  # Execute once: random.randrange(1 << 30, 1 << 31)
DECK_ID = 2125805380  # Execute once: random.randrange(1 << 30, 1 << 31)


logging.basicConfig(level=logging.INFO)


# Model for flashcards
model = genanki.Model(
    MODEL_ID,
    'Generated Vocab Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ]
)


def read_vocab(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    vocab = []
    for line in lines:
        parts = line.split('-')
        parts = [s.strip() for s in parts]
        assert len(parts) == 2, 'Should only have to parts'
        vocab += [parts]

    return vocab


def add_reversed_pairs(vocab):
    new_vocab = []
    for pair in vocab:
        new_vocab += [pair, pair[::-1]]
    return new_vocab



def main():
    parser = ArgumentParser()
    parser.add_argument('--input', help='Input file containing vocabulary')
    parser.add_argument('--output', help='Where to store the generated flashcards')
    parser.add_argument('--deck_id', help='Deck id to use when creating the deck', default=DECK_ID)
    parser.add_argument('--deck_name', help='Deck name to use when creating the deck', default='Vocabulary')
    parser.add_argument('--add_reversed', action='store_true', help='If set, also adds reversed direction of the vocab to the deck')
    args = parser.parse_args()

    # Load vocab
    vocab = read_vocab(args.input)
    logging.info('Found %i vocabulary entries in %s' % (len(vocab), args.input))

    if args.add_reversed:
        vocab = add_reversed_pairs(vocab)

    # Generate notes
    notes = []
    for pair in vocab:
        note = genanki.Note(
            model=model,
            fields=pair
        )
        notes.append(note)

    # Generate deck
    deck = genanki.Deck(
        args.deck_id,
        args.deck_name
    )
    for note in notes:
        deck.add_note(note)

    # Write file
    genanki.Package(deck).write_to_file(args.output)
    logging.info('Written deck with %i notes to %s' % (len(notes), args.output))


if __name__ == '__main__':
    main()
