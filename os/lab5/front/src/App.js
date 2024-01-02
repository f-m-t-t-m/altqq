import React, { useState, useEffect } from 'react';
import axios from 'axios'
import './App.css';
import DatePicker from 'react-datepicker';
import "react-datepicker/dist/react-datepicker.css";
import Plot from 'react-plotly.js';


function App() {
	const [temp, setTemp] = useState();
	const [startDateTime, setStartDateTime] = useState(new Date());
	const [endDateTime, setEndDateTime] = useState(new Date())
	const [plotUrl, setPlotUrl] = useState("");
	
	const[x, setX] = useState([]);
	const[y, setY] = useState([]);
	
	const baseUrl = "http://127.0.0.1";

	const updateTemp = () => {
		axios.get(baseUrl + "/current-temp").then((response) => {
			setTemp(response.data.currentTemp);
		});
	}
	
	useEffect(() => {
		updateTemp();
		setInterval(updateTemp, 1000);
	}, []);
	
	
	useEffect(() => {
		const url = baseUrl + "/temp-for-period" + (plotUrl ? "/" + plotUrl  : "") + "?start="+startDateTime.toLocaleString() + "&end="+endDateTime.toLocaleString();
		axios.get(url).then(response => {
			if (response.data) {
				const xs = [];
				const ys = [];
				for (const el of response.data) {
					xs.push(el.date);
					ys.push(el.temp);
				}
				setX(xs);
				setY(ys);
			} else {
				setX([]);
				setY([]);
			}
		})
	}, [startDateTime, endDateTime, plotUrl]);

	
	
	return (
	<div>
		Текущая температура: {temp}
		<div>
		Тип графика:
		<select
			onChange={e => setPlotUrl(e.target.value)}
		>
			<option value="">Текущая температура</option>
			<option value="avg-hour">Средняя температура за час</option>
			<option value="avg-day">Средняя температура за день</option>
		</select>
		</div>
		<div>
		Начало: 
		<DatePicker
			selected={startDateTime}
			onChange={(date) => {
				setStartDateTime(date);
			}}
			showTimeSelect
			timeFormat="HH:mm"
			timeIntervals={1}
			dateFormat="yyyy/MM/dd HH:mm"
		/>
		Конец:
		<DatePicker
			selected={endDateTime}
			onChange={(date) => {
				setEndDateTime(date);
			}}
			showTimeSelect
			timeFormat="HH:mm"
			timeIntervals={1}
			dateFormat="yyyy/MM/dd HH:mm"
		/>
		</div>
		<Plot
		data={[
		  {
			x: x,
			y: y,
			type: 'scatter',
			mode: 'lines+markers',
			marker: {color: 'red'},
		  },
		]}
		layout={ {width: 1000, height: 500} }
		/>
		</div>
	);
}

export default App;
