__author__ = 'SteamPowered'

class BruijnGraph:
    def __init__(self, text, k):
        '''
        Creates de Bruijn objects of a text input.
        :param text: any string
        :param k: kmer length
        :return:
        '''
        self.text = text
        self.k = k
        self.kmers = {}
        self.kmer_links = {}
        text_len = len(self.text)
        last_kmer = None
        self.kmer_links[None] = []
        self.boundaries = (text[:self.k], text[-self.k:])
        for i in range(0, text_len-self.k+1, 1):
            kmer = self.text[i:i+self.k]
            try:
                self.kmers[kmer].append((i, i+self.k))
            except KeyError:
                self.kmers[kmer] = [(i, i+self.k)]
            try:
                self.kmer_links[last_kmer].append(kmer)
            except KeyError:
                self.kmer_links[last_kmer] = [kmer]
            last_kmer = kmer
        print "Text is now a Graph!"

class CombineGraphs:
    def __init__(self, text_dict, k):
        '''
        Creates graphs for every given text.
        :param text_dict: A dictionary input with text name as keys and text as values.
        :param k: kmer length
        :return:
        '''
        self.csv_node_lines = []
        self.csv_rel_lines = []
        self.ids = {}
        self.k = k
        self.graphs = {}
        self.combined_graph = {}
        self.combined_kmers = {}
        self.id = 0
        self.annotations = {}
        for graph_name in text_dict:
            gr = None
            gr = BruijnGraph(text_dict[graph_name], self.k)
            self.graphs[graph_name] = gr

    def id_caster(self, value):
        '''
        Casts new id to increment current id.
        :param value: value to increase by. integer
        :return:
        '''
        self.id += value

    def combine(self):
        '''
        Combines the graphs into one graph.
        :return:
        '''
        for graph_name in self.graphs:
            for node in self.graphs[graph_name].kmer_links:
                try:
                    self.combined_graph[node] += self.graphs[graph_name].kmer_links[node]
                    self.combined_graph[node] = list(set(self.combined_graph[node]))
                except KeyError:
                    self.combined_graph[node] = self.graphs[graph_name].kmer_links[node]
                    self.ids[node] = self.id
                    self.id_caster(1)
                try:
                    self.combined_kmers[node].append(graph_name)
                except KeyError:
                    self.combined_kmers[node] = [graph_name]
        print 'Combined Graphs!'

    def combine_annotations(self):
        return None

    def create_csv_headers(self):
        node_header = ''   # <---------- Put the neo4j csv headers
        rel_header = ''
        self.csv_node_lines.append(node_header)
        self.csv_rel_lines.append(rel_header)

    def add_csv_lines(self):
        return None


if __name__ == "__main__":

    td = {'mice.cox1': 'MAAAAASLRRTVLGPRGVGLPGASAPGLLGGARSRQLPLRTPQAVSLSSKSGPSRGRKVML'
                  'SALGMLAAGGAGLAVALHSAVSASDLELHPPSYPWSHRGLLSSLDHTSIRRGFQVYKQVCS'
                  'SCHSMDYVAYRHLVGVCYTEEEAKALAEEVEVQDGPNDDGEMFMRPGKLSDYFPKPYPNPE'
                  'AARAANNGALPPDLSYIVRARHGGEDYVFSLLTGYCEPPTGVSLREGLYFNPYFPGQAIGM'
                  'APPIYTEVLEYDDGTPATMSQVAKDVATFLRWASEPEHDHRKRMGLKMLLMMGLLLPLTYA'
                  'MKRHKWSVLKSRKLAYRPPK',

          'human.cox1': 'MAAAAASLRGVVLGPRGAGLPGARARGLLCSARPGQLPLRTPQAVALSSKSGLSRGRKVM'
                   'LSALGMLAAGGAGLAMALHSAVSASDLELHPPSYPWSHRGLLSSLDHTSIRRGFQVYKQV'
                   'CASCHSMDFVAYRHLVGVCYTEDEAKELAAEVEVQDGPNEDGEMFMRPGKLFDYFPKPYP'
                   'NSEAARAANNGALPPDLSYIVRARHGGEDYVFSLLTGYCEPPTGVSLREGLYFNPYFPGQ'
                   'AIAMAPPIYTDVLEFDDGTPATMSQIAKDVCTFLRWASEPEHDHRKRMGLKMLMMMALLV'
                   'PLVYTIKRHKWSVLKSRKLAYRPPKK'}

    print (len(td['human'])+len(td['mice']))/2
    cg = CombineGraphs(td, 5)
    cg.combine()
    print cg.graphs['human'].boundaries
    print len(cg.combined_kmers)
    print len(cg.ids)

