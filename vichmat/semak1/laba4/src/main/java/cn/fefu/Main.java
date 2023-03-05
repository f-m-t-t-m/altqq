package cn.fefu;

import org.apache.commons.math3.analysis.differentiation.DerivativeStructure;
import org.apache.commons.math3.analysis.differentiation.UnivariateDifferentiableFunction;
import org.apache.commons.math3.analysis.function.Constant;
import org.apache.commons.math3.util.CombinatoricsUtils;

import java.util.*;
import java.util.function.*;

public class Main {

    private static double a = 0.4;

    private static double b = 0.9;

    private static double h = (b - a) / 10;

    private static class Func implements Function<Double, Double> {

        @Override
        public Double apply(Double x) {
            return Math.pow(x, 2) + Math.log(x);
        }

    }

    private static ArrayList<Double> getGrid() {
        ArrayList<Double> grid = new ArrayList<>();
        for(int i = 0; i <= 10; ++i) {
            grid.add(a + i * h);
        }
        return grid;
    }

    public static ArrayList<Double> findNClosestValues(ArrayList<Double> grid, double x, int count) {
        ArrayList<Double> xs = new ArrayList<>();
        for(int i = 1; i < grid.size(); ++i) {
            if (grid.get(i) > x) {
                int l = i - 2;
                int r = i + 1;
                xs.add(grid.get(i-1));
                xs.add(grid.get(i));
                while (xs.size() != count && (l >= 0 || r <= grid.size() - 1)) {
                    if ( l < 0 && r <= grid.size() - 1) {
                        xs.add(grid.get(r++));
                    } else if ( l >= 0 && r > grid.size() - 1) {
                        xs.add(0, grid.get(l--));
                    } else {
                        if (Math.abs(grid.get(l) - x) < Math.abs(grid.get(r) - x)) {
                            xs.add(0, grid.get(l--));
                        }
                        else {
                            xs.add(grid.get(r++));
                        }
                    }
                }
                break;
            }
        }
        return xs;
    }

    private static double lagrange(ArrayList<Double> grid, double x, Function<Double, Double> func,
                            int order) {
        ArrayList<Double> xs = findNClosestValues(grid, x, order + 1);
        DerivativeStructure x_ = new DerivativeStructure(1, 2, 0, x);
        DerivativeStructure res = new DerivativeStructure(1, 2);

        for (Double xValue1: xs) {
            double numerator = func.apply(xValue1);
            double denominator = 1.;
            DerivativeStructure localDerivative = new DerivativeStructure(0, x_, 1, x_.pow(0));
            for(Double xValue2: xs) {
                if (!xValue1.equals(xValue2)) {
                    localDerivative = localDerivative.multiply(x_.subtract(xValue2));
                    denominator *= (xValue1 - xValue2);
                }
            }
            localDerivative = localDerivative.multiply(numerator);
            localDerivative = localDerivative.divide(denominator);
            res = res.add(localDerivative);
        }
        return res.getPartialDerivative(1);
    }

    private static double getFuncDerivative(double x, int order) {
        DerivativeStructure x_ = new DerivativeStructure(1, order, 0, x);
        DerivativeStructure der = x_.pow(2).add(x_.log());
        return der.getPartialDerivative(order);
    }

    private static ArrayList<Double> getRemainders(ArrayList<Double> grid, double x, int order) {
        ArrayList<Double> xs = findNClosestValues(grid, x, order + 1);
        ArrayList<Double> res = new ArrayList<>();

        DerivativeStructure x_ = new DerivativeStructure(1, 2, 0, x);
        DerivativeStructure w = new DerivativeStructure(0, x_, 1, x_.pow(0));
        for(double xValue: xs) {
            double num = getFuncDerivative(xValue, order + 1) / CombinatoricsUtils.factorial(order + 1);
            res.add(num);
            w = w.multiply(x_.subtract(xValue));
        }
        for(int i = 0; i < res.size(); ++i) {
            res.set(i, Math.abs(res.get(i) * w.getPartialDerivative(1)));
        }
        return res;
    }
    public static void main(String[] args) {
        ArrayList<Double> grid = getGrid();
        System.out.println("L'(x) =         " + lagrange(grid, 0.4, new Func(), 3));
        System.out.println("f'(x) =         " +  getFuncDerivative(0.4, 1));
        System.out.println("L'(x) - f'(x) = "
                + Math.abs(lagrange(grid, 0.4, new Func(), 3) - getFuncDerivative(0.4, 1)));
        System.out.println("Min R'(x) =     " + Collections.min(getRemainders(grid, 0.4, 3)));
        System.out.println("Max R'(x) =     " + Collections.max(getRemainders(grid, 0.4, 3)));
    }

}