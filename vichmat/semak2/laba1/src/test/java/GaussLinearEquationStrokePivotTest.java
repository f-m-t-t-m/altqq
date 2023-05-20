import org.example.GaussLinearEquationSolverStrokePivot;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class GaussLinearEquationStrokePivotTest {

    double[][] a = {{2, 1, -1},
                    {-3, -1, 2},
                    {-2, 1, 2}};
    double[] b = {8, -11, -3};
    double[] expected = {2, 3, -1};

    @Test
    void test_get_stroke_pivot() {
        GaussLinearEquationSolverStrokePivot solver = new GaussLinearEquationSolverStrokePivot();
        assertEquals(0, solver.getStrokePivot(a, 0));
        assertEquals(2, solver.getStrokePivot(a, 1));
        assertEquals(2, solver.getStrokePivot(a, 2));
    }

    @Test
    void test_stroke_pivot() {
        GaussLinearEquationSolverStrokePivot solver = new GaussLinearEquationSolverStrokePivot();
        double[] actual = solver.solve(a, b);
        for (int i = 0; i < actual.length; ++i) {
            actual[i] = Math.round(actual[i] * 1e6) / 1e6;
        }
        assertArrayEquals(expected, actual);
    }


}
