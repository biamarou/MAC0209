import org.opensourcephysics.controls.*;
import org.opensourcephysics.frames.*;

public class FreewayApp2LaneTruck extends AbstractSimulation {

    Freeway2LaneTruck freeway = new Freeway2LaneTruck();
    DisplayFrame display = new DisplayFrame ("Freeway");
    LatticeFrame spaceTime = new LatticeFrame ("space", "time", "Space Time Diagram");

    public FreewayApp2LaneTruck() {
        display.addDrawable(freeway) ;
    }

    public void initialize () {
        int car_cnt = control.getInt("Number of cars");
        int truck_cnt = control.getInt("Number of trucks");
        int types[] = {car_cnt, truck_cnt};
        freeway.numberOfType = types;
        freeway.numberOfAutos = car_cnt + truck_cnt;
        freeway.roadLength = control.getInt("Road length");
        freeway.p = control.getDouble("Slow down probability");
        int car_max = control.getInt("Maximum car velocity");
        int truck_max = control.getInt("Maximum truck velocity");
        int maxvel[] = {car_max, truck_max};
        freeway.maxVelOfType = maxvel;
        display.setPreferredMinMax(0, freeway.roadLength, -3, 4);
        freeway.initialize(spaceTime);
    }

    public void doStep () {
        freeway.step();
    }

    public void reset () {
        control.setValue("Number of cars", 10);
        control.setValue("Number of trucks", 10);
        control.setValue("Road length", 50);
        control.setValue("Slow down probability" , 0.5);
        control.setValue("Maximum car velocity" , 4 );
        control.setValue("Maximum truck velocity" , 2 );
        control.setValue("Steps between plots" , 1);
        enableStepsPerDisplay(true);
    }

    public void resetAverages () {
        freeway.flow = 0;
        for (int i = 0; i < freeway.flows.length; i++)
            freeway.flows[i] = 0;
        freeway.steps = 0;
    }

    public static void main (String [] args) {
        SimulationControl control =
                SimulationControl.createApp (new FreewayApp2LaneTruck());
        control.addButton("resetAverages", "resetAverages");
    }
}
