import org.opensourcephysics.controls.*;
import org.opensourcephysics.frames.*;

public class FreewayAppFundamental extends AbstractSimulation {

    Freeway freeway = new Freeway ();
    DisplayFrame display = new DisplayFrame ("Freeway");
    LatticeFrame spaceTime = new LatticeFrame ("space", "time", "Space Time Diagram");
    LatticeFrame velDist = new LatticeFrame ("velocity", "cars", "Velocity distribution Diagram");
    LatticeFrame gapDist = new LatticeFrame ("gap size", "gaps", "Gap distribution Diagram");

    public FreewayAppFundamental () {
        display.addDrawable(freeway) ;
    }

    public void initialize () {
        freeway.numberOfCars = control.getInt("Number of cars");
        freeway.roadLength = control.getInt("Road length");
        freeway.p = control.getDouble("Slow down probability");
        freeway.maximumVelocity = control.getInt("Maximum velocity");
        display.setPreferredMinMax(0, freeway.roadLength, -3, 4);
        freeway.initialize(spaceTime, velDist, gapDist);
    }

    public void doStep () {
        if (freeway.steps == 1000) System.out.println(
                freeway.numberOfCars + " " + ((double)freeway.numberOfCars/freeway.roadLength)
                + " " + (double)freeway.flow/(freeway.steps*freeway.roadLength));
        else if (freeway.steps > 1000) return;
        freeway.step();
    }

    public void reset () {
        control.setValue("Number of cars", 10);
        control.setValue("Road length", 50);
        control.setValue("Slow down probability" , 0.5);
        control.setValue("Maximum velocity" , 2 );
        control.setValue("Steps between plots" , 1);
        enableStepsPerDisplay(true);
    }

    public void resetAverages () {
        freeway.flow = 0;
        freeway.steps = 0;
    }

    public static void main (String [] args) {
        SimulationControl control =
        SimulationControl.createApp (new FreewayAppFundamental());
        control.addButton("resetAverages", "resetAverages");
    }
}
