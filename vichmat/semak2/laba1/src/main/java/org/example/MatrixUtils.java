package org.example;

import java.util.Arrays;

public class MatrixUtils {

    public static boolean isMatrixTriangular(double[][] a) {
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < i; ++j) {
                if (Math.abs(a[i][j] - 0.0) > 10e-7d) {
                    return false;
                }
            }
        }
        return true;
    }

    public static double[] copyAndMultiplyArray(double[] a, double multiplier) {
        double[] aCopy = Arrays.copyOf(a, a.length);
        for(int i = 0; i < aCopy.length; ++i) {
            aCopy[i] *= multiplier;
        }
        return aCopy;
    }

    public static void subtractLine(double[] a, double[] b) {
        for(int i = 0; i < a.length; ++i) {
            a[i] -= b[i];
        }
    }

    public static void printMatrix(double[][] a) {
        for(double[] row: a) {
            for(double col: row) {
                System.out.printf("%f ", col);
            }
            System.out.println();
        }
        System.out.println();
    }

    public static double[][] multiply(double[][] a, double[][] b) {
        int m = a.length;
        int n = b[0].length;
        double[][] res = new double[m][n];
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                for (int k = 0; k < m; ++k) {
                    res[i][j] += a[i][k]*b[k][j];
                }
            }
        }
        return res;
    }

    public static double[][] transpose(double[][] a) {
        double[][] res = new double[a[0].length][a.length];
        for (int i = 0; i < a.length; ++i) {
            for (int j = 0; j < a[0].length; ++j) {
                res[j][i] = a[i][j];
            }
        }
        return res;
    }

    public static double norm(double[] vec) {
        double sum = 0;
        for (double v : vec) {
            sum += Math.pow(v, 2);
        }
        return Math.sqrt(sum);
    }

    public static double[] plus(double[] v1, double[] v2) {
        double[] res = new double[v1.length];
        for (int i = 0 ; i < v1.length; ++i) {
            res[i] = v1[i] + v2[i];
        }
        return res;
    }

    public static double[] minus(double[] v1, double[] v2) {
        double[] res = new double[v1.length];
        for (int i = 0 ; i < v1.length; ++i) {
            res[i] = v1[i] - v2[i];
        }
        return res;
    }

    public static double[] divide(double[] vec, double divider) {
        double[] res = vec.clone();
        for (int i = 0; i < vec.length; ++i) {
            res[i] /= divider;
        }
        return res;
    }

    public static double[] product(double[] vec, double val) {
        double[] res = vec.clone();
        for (int i = 0; i < vec.length; ++i) {
            res[i] *= val;
        }
        return res;
    }

    public static double scalarProduct(double[] a, double[] b) {
        double res = 0;
        for (int i  = 0; i < a.length; ++i) {
            res += a[i] * b[i];
        }
        return res;
    }

    public static double max(double[] a) {
        double m = Double.MIN_VALUE;
        for (int i = 0; i < a.length; i++) {
            m = Math.max(a[i], m);
        }
        return m;
    }

    private MatrixUtils() {
    }

}
