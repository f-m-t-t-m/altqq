package org.example;

import static org.example.MatrixUtils.*;

public class GaussLinearEquationWithMainElementSolver extends GaussLinearEquationSolver {

    @Override
    protected void forwardStep(double[][] a, double[] b) {
        int lastIndexA = a.length - 1;
        for(int i = 0; i < lastIndexA; ++i) {
            if (isMatrixTriangular(a)) {
                return;
            }
            swapRows(a, b, getRowNumberOfMaxElement(a, i), i);
            for(int j = i + 1; j < a.length; ++j) {
                double multiplier = a[j][i]/a[i][i];
                double[] subtractLineA = copyAndMultiplyArray(a[i], multiplier);
                b[j] -= b[i]*multiplier;
                subtractLine(a[j], subtractLineA);
            }
        }
    }

    private int getRowNumberOfMaxElement(double[][] a, int colNumber) {
        int idxOfMax = 0;
        for (int row = 1; row < a.length; ++row) {
            idxOfMax = a[row][colNumber] > a[idxOfMax][colNumber] ? row : idxOfMax;
        }
        return idxOfMax;
    }

    private void swapRows(double[][] a, double[] b, int from, int to) {
        double[] tmpA = a[to];
        a[to] = a[from];
        a[from] = tmpA;

        double tmpB = b[to];
        b[to] = b[from];
        b[from] = tmpB;
    }

}
