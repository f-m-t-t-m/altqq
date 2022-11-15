package cn.fefu;

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

    public static void main(String[] args) {

    }

}
