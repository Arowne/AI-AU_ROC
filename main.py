class AU_ROC():

    def __init__(self, inputs=None, treshold=None, probability=None):
        self.input = inputs
        self.treshold = treshold
        self.model_probability_output_simulation = probability
        self.model_prediction = []
        self.fpr = []
        self.tpr = []

    def set_treshold(self, treshold_array):
        self.treshold = treshold_array
    
    def set_input(self, inputs):
        self.input = inputs
    
    def set_model_probality_output_simulation(self, probability):
        self.model_probability_output_simulation = probability

    def get_treshold(self):
        return self.treshold
    
    def get_input(self):
        return self.input
    
    def get_model_probality_output_simulation(self):
        return self.model_probability_output_simulation
    
    def params_validator(self):

        probality = self.model_probability_output_simulation
        if len(probality) != len(self.input):
            print('Error at row ' + str(probality) + '. Your probality row must have the same length as your input')

    def set_model_predictions(self):
        self.model_prediction = []
        for x in range(len(self.treshold)):
            get_model_prediction = []
            treshold = self.treshold[x]

            for i in range(len(self.model_probability_output_simulation)):
                probability = self.model_probability_output_simulation[i]
                if probability > treshold:
                    get_model_prediction.append(1)
                else:
                    get_model_prediction.append(0)

            self.model_prediction.append(get_model_prediction)
    
    def get_model_predictions(self):
        return self.model_prediction

    # tpr = tp + fn / tp
    def set_tpr(self):
        tp = 0
        fn = 0
        for i in range(len(self.model_prediction)):
            tp = 0
            fn = 0
            for j in range(len(self.model_prediction[i])):
                prediction = self.model_prediction[i][j]
                value = self.input[j]
                if value == 1 and prediction == 1:
                    tp = tp + 1
                elif value == 1 and prediction == 0:
                    fn = fn + 1
            self.tpr.append(tp / (tp + fn))
    
    # fpr = fp + tn / fp
    def set_fpr(self):
        fp = 0
        tn = 0
        for i in range(len(self.model_prediction[0])):
            fp = 0
            tn = 0
            for j in range(len(self.model_prediction[i])):
                prediction = self.model_prediction[i][j]
                value = self.input[j]
                if value == 0 and prediction == 0:
                    fp = fp + 1
                elif value == 0 and prediction == 1:
                    tn = tn + 1
            self.fpr.append(fp / (tn + fp))

    def get_best_treshold(self):
        max_fpr = 0
        best_model_fpr_candidates = []
        for x in range(len(self.treshold)):
            if self.fpr[x] > max_fpr:
                max_fpr = self.fpr[x]
                best_model_fpr_candidates = []
                best_model_fpr_candidates.append(x)
            elif self.fpr[x] == max_fpr:
                best_model_fpr_candidates.append(x)

        max_tpr = 0
        best_model_candidates = []
        best_model_candidates_index = 0
        for x in range(len(best_model_fpr_candidates)):
            if self.tpr[best_model_fpr_candidates[x]] >= max_tpr:
                max_tpr = self.tpr[best_model_fpr_candidates[x]]
                best_model_candidates.append(x)
                best_model_candidates_index = best_model_fpr_candidates[x]

        print("best prediction => " + str(self.model_prediction[best_model_candidates_index]))
        print("best treshold => " + str(self.treshold[best_model_candidates_index]))

    def get_results(self):
        print(self.input)
        print(self.treshold)
        print("\n")
        for x in range(len(self.treshold)):
            print("\n")
            print("######### " + str(self.treshold[x]) + " ##########")
            print(str(self.model_prediction[x]))
            print("tpr: " + str(self.tpr[x]) + "; fpr: " + str(self.fpr[x]))
        
if __name__ == "__main__":
    auroc = AU_ROC()
    auroc.set_input([1, 1, 1, 0, 1, 1, 0, 1, 0])
    auroc.set_treshold([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    auroc.set_model_probality_output_simulation([0.6, 0.7, 0.8, 0.2, 0.5, 0.9, 0.4, 0.6, 0.3])
    auroc.params_validator()
    auroc.set_model_predictions()
    model_prediction = auroc.get_model_predictions()
    auroc.fpr
    auroc.set_fpr()
    auroc.set_tpr()
    auroc.get_results()
    auroc.get_best_treshold()

