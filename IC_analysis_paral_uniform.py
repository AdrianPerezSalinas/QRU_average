from IC_analysis_uniform import main
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('--seed', type=int, default=0)


if __name__ == '__main__':
    seed = vars(parser.parse_args())['seed']
    nqubits_list = [4, 6, 8, 10, 12]
    nlayers_list = [4, 8, 12, 20]
    models = [1, 2]
    seed_num = 10
    
    model_num = seed // (len(nqubits_list) * len(nlayers_list) * seed_num)
    seed = seed % (len(nqubits_list) * len(nlayers_list) * seed_num)
    model = models[model_num]

    q = seed // (len(nlayers_list) * seed_num)
    seed = seed % (len(nlayers_list) * seed_num)
    nqubits = nqubits_list[q]

    l = seed // (seed_num)
    seed = seed % (seed_num)
    nlayers = nlayers_list[l]

    extra_dim = 10
    data_size = 10

    main(nqubits, nlayers, model, seed)
