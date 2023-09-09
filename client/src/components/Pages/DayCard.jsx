import ListGroup from "react-bootstrap/ListGroup";
import { useEffect, useState } from "react";
import useUserStore from "../../hooks/useStore";

export default function DayCard() {
  const { user } = useUserStore();
  //   console.log(`logged in`, user.tfp_pay);
  const [dayObj, setDayObj] = useState();
  useEffect(() => {
    fetch(`/api/days/1`)
      .then((response) => response.json())
      .then((data) => {
        console.log(`this is the day object`, data);
        setDayObj(data);
      });
  }, []);
  //   console.log(dayObj, "this is the dayObj");

  //=============Rate Calc===================================
  function rateCalculator(dayObject, factors) {
    // Create a copy of the dayObject to avoid mutating the original object
    const updatedDayObject = { ...dayObject };

    // Iterate through the keys in the dayObject
    for (const key in updatedDayObject) {
      if (updatedDayObject.hasOwnProperty(key)) {
        // Check if the value is an integer and if there's a corresponding factor in the factors dictionary
        if (typeof updatedDayObject[key] === "number" && factors[key]) {
          // Multiply the integer value by the factor
          updatedDayObject[key] *= factors[key];
        }
      }
    }

    return updatedDayObject;
  }

  const factors = {
    a_hours: user.a_postion_pay,
    daily_duty_hours: 1,
    double_half: 2.5,
    double_time: 2,
    holiday: 1.5,
    overrides: user.override_pay,
    time_half: 1.5,
    total_tfp: 1,
    triple: 3,
    vacation_sick: 1,
    vja: 1.5,
  };

  const updatedDay = rateCalculator(dayObj, factors);
  console.log(`updated day`, updatedDay);

  // Calculate payObj values
  const a_hours = updatedDay.a_hours;
  const overrides = updatedDay.overrides;
  const otherIntValues = Object.entries(updatedDay)
    .filter(
      ([key, value]) =>
        typeof value === "number" &&
        key !== "a_hours" &&
        key !== "overrides" &&
        key !== "id"
    )
    .reduce((accumulator, [key, value]) => {
      accumulator[key] = (value * user.tfp_pay)?.toFixed(2); // Round to two decimal places
      return accumulator;
    }, {});

  // Calculate the sum of a_hours and overrides
  const a_hoursAndOverrides = a_hours + overrides;

  // Construct the payObj
  const payObj = {
    a_hours: a_hours?.toFixed(2), // Round to two decimal places
    overrides: overrides?.toFixed(2), // Round to two decimal places
    id: updatedDay.id, // Include the id property
    ...otherIntValues,
  };

  console.log(payObj);

  return (
    <div>
      {" "}
      <ListGroup>
        <ListGroup.Item>Cras justo odio</ListGroup.Item>
        <ListGroup.Item>Dapibus ac facilisis in</ListGroup.Item>
        <ListGroup.Item>Morbi leo risus</ListGroup.Item>
        <ListGroup.Item>Porta ac consectetur ac</ListGroup.Item>
        <ListGroup.Item>Vestibulum at eros</ListGroup.Item>
      </ListGroup>
    </div>
  );
}

// const daysArray = [
//   // ... your array of day objects
// ];

// // Define a function to calculate the value for a specific category
// const calculateCategoryValue = (category, day) => {
//   switch (category) {
//     case 'a_hours':
//       return day.a_hours * 2; // Multiply a_hours by 2
//     // Add more cases for other categories and their respective multipliers
//     // case 'other_category':
//     //   return day.other_category * multiplier;
//     default:
//       return 0; // Default to 0 if category not found
//   }
// };

// // Define a function to calculate the total value for a specific category in the array
// const calculateCategoryTotal = (category) => {
//   return daysArray.reduce((total, day) => total + calculateCategoryValue(category, day), 0);
// };

// // Usage:
// const totalAHours = calculateCategoryTotal('a_hours'); // Total for 'a_hours'
// // Calculate totals for other categories as needed

// function YourComponent() {
//   return (
//     <div>
//       <p>Total for a_hours: {totalAHours}</p>
//       {/* Display totals for other categories here */}
//     </div>
//   );
// }

// export default YourComponent;
