package org.example;

import static org.example.MatrixUtils.*;

public class GaussLinearEquationSolverColumnPivot extends GaussLinearEquationSolver {

    @Override
    public void forwardStep(double[][] a, double[] b) {
        int lastIndexA = a.length - 1;
        for(int i = 0; i < lastIndexA; ++i) {
            swapRows(a, b, getColumnPivot(a, i), i);
            if (a[i][i] == 0) {
                throw new ArithmeticException(String.format("В результате преобразований на " +
                        "%d строке диагональный элемент равен 0", i+1));
            }
            for(int j = i + 1; j < a.length; ++j) {
                double multiplier = a[j][i]/a[i][i];
                double[] subtractLineA = copyAndMultiplyArray(a[i], multiplier);
                b[j] -= b[i]*multiplier;
                subtractLine(a[j], subtractLineA);
            }
        }
        if (a[lastIndexA][lastIndexA] == 0) {
            throw new ArithmeticException(String.format("В результате преобразований на " +
                    "%d строке диагональный элемент равен 0", lastIndexA+1));
        }
    }

    public int getColumnPivot(double[][] a, int colNumber) {
        int idxOfMax = colNumber;
        for (int row = colNumber; row < a.length; ++row) {
            idxOfMax = Math.abs(a[row][colNumber]) > Math.abs(a[idxOfMax][colNumber]) ? row : idxOfMax;
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
