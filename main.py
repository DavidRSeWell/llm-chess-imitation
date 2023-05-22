from src.data_processing.create_vocab_models import create_vocab, save_vocab

def main(source_file, vocab_dir, add_piece_type = True, notation = "uci"):

    vocab = create_vocab(source_file, add_piece_type, notation=notation)
    save_vocab(vocab, notation, vocab_dir)




if __name__ == "__main__":
    source_file = "/Users/davidsewell/Data/Chess/millonbase/millionbase-2.5_uci_processed.txt"
    vocab_dir = "/Users/davidsewell/Data/Chess/millonbase/"
    main(source_file, vocab_dir)
