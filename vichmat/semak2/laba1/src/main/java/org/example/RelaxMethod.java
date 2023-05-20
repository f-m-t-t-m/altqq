package org.example;

public class RelaxMethod extends SimpleIteration {

    @Override
    protected double[] calcNewX(double[][] a, double[] b, double[] oldX, double[][] solveMatrix) {
        double omega = 1.1;
        double[] newX = new double[b.length];
        double[] oldXCopy = oldX.clone();
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < b.length; ++j) {
                newX[i] += solveMatrix[i][j] * oldXCopy[j];
            }
            newX[i] += b[i];
            newX[i] *= omega/a[i][i];
            newX[i] += oldXCopy[i] * (1 - omega);
            oldXCopy[i] = newX[i];
        }
        return newX;
    }

}
