import sys
import csv
from os.path import join as opj
from sklearn.metrics import precision_recall_curve, auc, roc_curve
import matplotlib.pyplot as plt
import json

def main():
    test_dir = sys.argv[1]
    pred_file = opj(test_dir, "results.csv")
    resp = []
    preds = []
    stats = {}
    lw = 2
    with open(pred_file) as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            resp.append(int(line[1]))
            preds.append(float(line[3]))

    fpr, tpr, _ = roc_curve(resp, preds, pos_label=1)
    stats["auc"] = auc(fpr, tpr)

    # adapted from https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=lw)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.savefig(opj(test_dir, "roc.png"))

    precision, recall, _ = precision_recall_curve(resp, preds)

    plt.figure()
    plt.step(recall, precision, alpha=0.2, color="b")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.savefig(opj(test_dir, "precision-recall.png"))

    with open(opj(test_dir, "stats.json"), "w") as f:
        f.write(json.dumps(stats))

main()