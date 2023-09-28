/* eslint-disable no-unused-vars */
//===========STATE MANAGMENT================
import { useEffect, useState } from "react";
import useUserStore from "../../hooks/useStore";
//========COMPONENTS===========================
import PairingCard from "./PairingCard";
import MonthPieChart from "./MonthPieChart";
import MonthBarGraph from "./MonthBarGraph";
import PairingAddModal from "./PairingAddModal";
import MonthTotalAll from "./MonthTotalAll";
//==========BOOTSTRAP IMPORTS ============
import { Col, Row, Container, Button, Modal, Form } from "react-bootstrap";
import Carousel from "react-bootstrap/Carousel";
import Dropdown from "react-bootstrap/Dropdown";
import ProgressBar from "react-bootstrap/ProgressBar";
import DeleteYearModal from "./DeleteYearModal";
import DeletePairingModal from "./DeletePairingModal";
export default function Dashboard() {
  //   const today = new Date();
  //   const start = today.getMonth() + 1;

  //================ZUSTAND STATE STUFF=================
  const { user } = useUserStore();
  // const [refreshOtherComponent, setRefreshOtherComponent] = useState(false);
  // const handlePostSuccess = () => {
  // setRefreshOtherComponent((prevRefresh) => !prevRefresh);
  // };
  //================STATE FOR DOM RENDER
  //=================================== usersYears THIS IS SET IN INITIAL FETCH REQUEST THIS IS WHATS MAPPED ON TO MAKE THE YEARS IN YEAR DROPDOWN. WHEN A DROPDOWN YEAR IS CLICKED, USERSMONTHS ARE SET
  const [usersYears, setUsersYears] = useState([]);
  //=================================== displayYear THIS IS SET WHEN USER CLICKS ON A YEAR FROM THE DROPDOWN I THINK ALL IT DOES IS DISPLAY THE YEAR ON THE BUTTON
  const [displayYear, setDisplayYear] = useState();
  //=================================== usersMonths THIS IS SET WHEN USER CLICKS ON A YEAR FROM THE DROPDOWN IT IS WHATS MAPPED TO MAKE THE MONTH BUTTONS
  const [usersMonths, setUsersMonths] = useState([]);

  //=================================== monthId THIS IS SET WHEN USER CLICKS ON A MONTH MAPPED FROM USERSMONTHS
  //====SEEMS TO BUT USED TO FILTER usersMonths AND SET THE DISPLAY MONTH
  const [monthId, setMonthId] = useState(0);
  //=================================== selectedMonthId THIS IS SET WHEN USER CLICKS ON A MONTH MAPPED FROM USERSMONTHS
  //====SEEMS TO BUT USED TO SHOW ACTIVE MONTH. MAYBE USELESS BUT I'M JUST GONNA LEAVE IT.
  const [selectedMonthId, setSelectedMonthId] = useState(null);
  // console.log(monthId);

  //=====================================testing some state that changes with delete pairing i can use as useEffect dependancy. SPOILER: it didn't work
  const [force, setForce] = useState(false);
  function forceReset(test) {
    setForce(!force);
  }

  //=================================================testing fetching state for graphs
  const [betterMonthState, setBetterMonthState] = useState({});

  //==========================================================LOCAL STORAGE GETTER
  // useEffect(() => {
  //   try {
  //     //===================USERS YEAR
  //     const userYears = window?.localStorage.getItem("USER_YEARS");
  //     if (userYears) {
  //       const parsedUserYears = JSON.parse(userYears);
  //       setDisplayYear(parsedUserYears);
  //     } else {
  //       setDisplayYear(null);
  //     }
  //     //===================DISPLAY YEAR
  //     const yearText = window?.localStorage.getItem("MY_Display_Year");
  //     if (yearText) {
  //       const parsedYear = JSON.parse(yearText);
  //       setDisplayYear(parsedYear);
  //     } else {
  //       setDisplayYear(null);
  //     }

  //     //===================USERS MONTHS
  //     const monthButtons = window?.localStorage.getItem("MY_MONTH_BUTTONS");
  //     if (monthButtons) {
  //       const parsedMonths = JSON.parse(monthButtons);
  //       setUsersMonths(parsedMonths);
  //     } else {
  //       setUsersMonths([]);
  //     }

  //     //===================MONTH ID (DUMB)
  //     const idForMonth = window?.localStorage.getItem("MY_MONTH_ID");
  //     if (idForMonth) {
  //       const parsedMonthId = JSON.parse(idForMonth);
  //       setMonthId(parsedMonthId);
  //     } else {
  //       setMonthId(null);
  //     }

  //     //===================SELECTED MONTH ID (REDUNDANT, BUT IT AIN'T BROKE)
  //     const idForSelectedMonth = window?.localStorage.getItem(
  //       "MY_SELECTED_MONTH_ID"
  //     );
  //     if (idForSelectedMonth) {
  //       const parsedSelectedMonthId = JSON.parse(idForSelectedMonth);
  //       setSelectedMonthId(parsedSelectedMonthId);
  //     } else {
  //       setSelectedMonthId(null);
  //     }
  //   } catch (error) {
  //     console.error("Error handling localStorage data:", error);
  //     // Handle the error as needed
  //   }
  // }, []);
  // //==========================================================LOCAL STORAGE SETTER
  // useEffect(() => {
  //   //===================USER YEAR
  //   window.localStorage.setItem("USER_YEARS", JSON.stringify(usersYears));
  //   //===================DISPLAY YEAR
  //   window.localStorage.setItem("MY_Display_Year", JSON.stringify(displayYear));
  //   //===================USERS MONTHS
  //   window.localStorage.setItem(
  //     "MY_MONTH_BUTTONS",
  //     JSON.stringify(usersMonths)
  //   );
  //   //===================MONTH ID (DUMB)
  //   window.localStorage.setItem("MY_MONTH_ID", JSON.stringify(monthId));
  //   //===================SELECTED MONTH ID (REDUNDAT, BUT IT AIN'T BROKE)
  //   window.localStorage.setItem(
  //     "MY_SELECTED_MONTH_ID",
  //     JSON.stringify(selectedMonthId)
  //   );
  // }, [usersYears, displayYear, usersMonths, monthId, selectedMonthId]);

  //=============MODAL STUFF======================
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const [yearObj, setYearObj] = useState({
    user_id: user.id,
    year: 0,
    year_a_hours: 0,
    year_a_pay: 0,
    year_double_half: 0,
    year_double_half_pay: 0,
    year_double_half_rated: 0,
    year_double_time: 0,
    year_double_time_pay: 0,
    year_double_time_rated: 0,
    year_duty_hours: 0,
    year_holiday: 0,
    year_holiday_pay: 0,
    year_holiday_rated: 0,
    year_int_tafb_pay: 0,
    year_int_tafb_total: 0,
    year_overrides: 0,
    year_overrides_pay: 0,
    year_tafb_pay: 0,
    year_tafb_total: 0,
    year_tfp: 0,
    year_tfp_pay: 0,
    year_time_half: 0,
    year_time_half_pay: 0,
    year_time_half_rated: 0,
    year_total_credits: 0,
    year_total_credits_rated: 0,
    year_total_pay: 0,
    year_triple: 0,
    year_triple_pay: 0,
    year_triple_rated: 0,
    year_vacation_sick: 0,
    year_vacation_sick_pay: 0,
    year_vja: 0,
    year_vja_pay: 0,
    year_vja_rated: 0,
  });
  const handleEdit = (e) => {
    e.preventDefault();
    handleClose();
    console.log("form submitting", yearObj);
    fetch("/api/years", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(yearObj),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response error");
        }
        return response.json();
      })
      .then((data) => {
        console.log("response data, prob the year?", data);

        setUsersYears([...usersYears, data]);

        setYearObj({
          user_id: user.id,
          year: 0,
          year_a_hours: 0,
          year_a_pay: 0,
          year_double_half: 0,
          year_double_half_pay: 0,
          year_double_half_rated: 0,
          year_double_time: 0,
          year_double_time_pay: 0,
          year_double_time_rated: 0,
          year_duty_hours: 0,
          year_holiday: 0,
          year_holiday_pay: 0,
          year_holiday_rated: 0,
          year_int_tafb_pay: 0,
          year_int_tafb_total: 0,
          year_overrides: 0,
          year_overrides_pay: 0,
          year_tafb_pay: 0,
          year_tafb_total: 0,
          year_tfp: 0,
          year_tfp_pay: 0,
          year_time_half: 0,
          year_time_half_pay: 0,
          year_time_half_rated: 0,
          year_total_credits: 0,
          year_total_credits_rated: 0,
          year_total_pay: 0,
          year_triple: 0,
          year_triple_pay: 0,
          year_triple_rated: 0,
          year_vacation_sick: 0,
          year_vacation_sick_pay: 0,
          year_vja: 0,
          year_vja_pay: 0,
          year_vja_rated: 0,
        });
      })
      .catch((error) => {
        console.log("error", error.message);
      });
  };
  //============= END MODAL STUFF======================

  //=============CAROUSEL STUFF======================
  const [index, setIndex] = useState(0);
  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
  };
  //============= END CAROUSEL STUFF======================
  //========================================================INITIAL USER FETCH SETS USERS YEARS
  useEffect(() => {
    fetch(`/api/users/${user.id}`)
      .then((response) => response.json())
      .then((data) => {
        setUsersYears(data.years_field);
      });
  }, [force, user.id]);

  //=============================MOSTLY USED IN GRAPHS/MODALS. SEEMS TO FIX SOME ASYNC ISSSUES
  // ============monthId is set when user clicks on month button mapped from USERSMONTHS
  // displayMonth is an array of one month. annoying, right?
  let displayMonth = usersMonths?.filter((month) => month.id === monthId);
  //==========betterMonth is same as displayMonth, just popped outta the array
  const betterMonth = displayMonth[0];
  // console.log("this is better month", betterMonth);
  //============tried doing betterPairings instead of passing betterMonth or displayMonth[0] but ran into async issues. so its unused.
  const betterPairings = betterMonth?.pairings_field;
  //========================================USED FOR PRGRESS BARS
  const guarantee_hours = displayMonth[0]?.month_guarantee_hours;
  const guarantee_hours_worked =
    displayMonth[0]?.month_guarantee_hours_worked_rated;
  //=============new new? ======================
  const [testMonth, setTestMonth] = useState({});
  useEffect(() => {
    fetch(`/api/months/${monthId}`)
      .then((response) => response.json())
      .then((data) => {
        setTestMonth(data);
        setBetterMonthState(data);
        // console.log(
        //   "this is betterMonthState we just fetched",
        //   betterMonthState
        // );
        // console.log('this is "betterMonth for graph"', betterMonth);
      });
  }, [monthId]);

  return (
    <>
      {" "}
      <Container>
        <Row className="mt-3 d-flex ">
          <Col xs="auto" className="mt-1">
            <h4>Selected Year:</h4>
          </Col>
          <Col xs="auto">
            <Dropdown>
              <Dropdown.Toggle variant="dark" id="dropdown-basic">
                {displayYear ? displayYear : "Select Year"}
              </Dropdown.Toggle>

              <Dropdown.Menu>
                {usersYears.map((year) => (
                  <Button
                    className="dropdown-item"
                    key={year.id}
                    onClick={(e) => {
                      setUsersMonths(year.months_field),
                        setDisplayYear(year.year);
                    }}
                  >
                    {year.year}
                  </Button>
                ))}
                <Dropdown.Divider />
                <>
                  <Button className="dropdown-item" onClick={handleShow}>
                    Add Year
                  </Button>
                  {<DeleteYearModal usersYears={usersYears} />}

                  <Modal show={show} onHide={handleClose} animation={false}>
                    <Modal.Header closeButton>
                      <Modal.Title>Create Year </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                      <Form onSubmit={handleEdit}>
                        <Form.Group controlId="exampleForm.ControlInput1">
                          {/* <Form.Label>Year</Form.Label> */}
                          <Form.Control
                            type="number"
                            placeholder="Enter year you wish to create..."
                            onChange={(e) =>
                              setYearObj({ ...yearObj, year: e.target.value })
                            }
                            // You can add additional attributes like min and max to limit the year range.
                            min="1900"
                            max="2099"
                          />
                        </Form.Group>
                      </Form>
                    </Modal.Body>
                    <Modal.Footer>
                      <Button variant="secondary" onClick={handleClose}>
                        Close
                      </Button>
                      <Button variant="dark" onClick={handleEdit}>
                        Save Changes
                      </Button>
                    </Modal.Footer>
                  </Modal>
                </>
                {/* <Dropdown.Item href="#action/3.4">Separated link</Dropdown.Item> */}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Row>
        <Row className="mt-3  d-flex flex-nowrap overflow-auto">
          {usersMonths.map((month) => (
            <Col key={month.id} className="px-0 px-1">
              <Button
                variant={month.id === selectedMonthId ? "custom" : "dark"}
                style={{
                  borderRadius: "0",
                  background: month.id === selectedMonthId ? "#a9d262" : "",
                  color: month.id === selectedMonthId ? "white !important" : "",
                }}
                key={month.id}
                onClick={() => {
                  setSelectedMonthId(month.id), setMonthId(month.id);
                }}
                className={`w-100 mb-2 ${
                  month.id === selectedMonthId ? "text-white" : ""
                }`}
              >
                {month.month}
              </Button>
            </Col>
          ))}
        </Row>
      </Container>
      {/* ===============================Month Pie chart========================== */}
      <Container className="m-0 p-0">
        <Row className="mt-5">
          <Col lg={4} className="border p-1 ">
            {betterMonth ? <MonthPieChart betterMonth={betterMonth} /> : null}
          </Col>
          {/* ===============================PROGRESS BARS========================== */}
          <Col lg={8} className="d-flex">
            <Container className="  m-0 p-0 text-center">
              <Row>
                <Container className="m-0 p-0">
                  {" "}
                  {guarantee_hours > 0 ? (
                    <ProgressBar
                      now={(guarantee_hours / guarantee_hours) * 100}
                      label={`${guarantee_hours} Guarantee Hours This Month`}
                      style={{ borderRadius: 0 }}
                      className="border rounded-0"
                    />
                  ) : null}
                  {guarantee_hours_worked > 0 ? (
                    <ProgressBar
                      animated
                      now={(guarantee_hours_worked / guarantee_hours) * 100}
                      label={`${guarantee_hours_worked} Guarantee Worked`}
                      style={{ borderRadius: 0 }}
                      className="border rounded-0"
                    />
                  ) : null}
                </Container>
              </Row>
              {/* ===============================Carousel========================== */}
              <Row className="justify-content-between  mt-2 ">
                <Col lg={7}>
                  {displayMonth[0]?.pairings_field.length > 0 ? (
                    <Carousel className="custom-carousel" interval={null}>
                      {displayMonth[0]?.pairings_field.map((pairing) => (
                        <Carousel.Item key={pairing.id}>
                          <div className="centered-card">
                            <PairingCard pairing={pairing} />
                          </div>
                        </Carousel.Item>
                      ))}
                    </Carousel>
                  ) : null}
                </Col>
                {/* ===============================BAR GRAPH MONTH========================== */}
                <Col lg={5} className="border p-1 ">
                  {betterMonth ? (
                    <MonthBarGraph
                      betterMonth={betterMonth}
                      betterMonthState={betterMonthState}
                      // refresh={refreshOtherComponent}
                    />
                  ) : null}
                  {betterMonth ? (
                    <PairingAddModal
                      displayMonth={displayMonth}
                      forceReset={forceReset}
                      // setForce={setForce}
                      // force={force}
                      // onPostSuccess={handlePostSuccess}
                    />
                  ) : null}
                  {betterMonth ? (
                    <DeletePairingModal
                      displayMonth={displayMonth}
                      forceReset={forceReset}
                      // setForce={setForce}
                      // force={force}
                      // onPostSuccess={handlePostSuccess}
                    />
                  ) : null}
                </Col>
              </Row>
            </Container>
          </Col>
        </Row>
        {/* ================Accordian Totals=================== */}
        <Row className="justify-content-center  mt-2 ">
          <Col className="border m-0 p-0">
            {displayMonth[0]?.pairings_field.length > 0 ? (
              <MonthTotalAll betterMonth={betterMonth} />
            ) : null}
          </Col>
        </Row>
      </Container>
    </>
  );
}
