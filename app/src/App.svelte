<script>
	// import svelteLogo from "./assets/svelte.svg"
	// import Counter from "./lib/Counter.svelte"
	import StatusBar from "./lib/StatusBar.svelte"
	import StatusIndicator from "./lib/StatusIndicator.svelte"
	import Chart from "chart.js/auto"
	import { io } from "socket.io-client"
	import { onMount } from "svelte"
	import Loader from "./lib/Loader.svelte"
	import Modal from "./lib/Modal.svelte"

	let chartCtx
	let chart
	let session
	let backendReady = false
	let recording = false
	let deleteModal = false
	let showModal = false

	const data = {
		datasets: [
			{
				label: "SPEED",
				borderColor: "#e22134",
				fill: false,
				tension: 0.1,
			},
			{
				label: "THROTTLE_POS",
				borderColor: "#3498DB",
				fill: false,
				tension: 0.1,
			},
			{
				label: "FUEL_LEVEL",
				borderColor: "#F1C40F",
				fill: false,
				tension: 0.1,
			},
			{
				label: "HYBRID_BATTERY_REMAINING",
				borderColor: "#9B59B6",
				fill: false,
				tension: 0.1,
			},
		],
	}

	const createChart = () => {
		data.labels = []
		data.datasets.forEach((dataset) => {
			dataset.data = []
		})
		const ctx = chartCtx.getContext("2d")
		// @ts-ignore
		chart = new Chart(ctx, { type: "line", data: data })
	}

	onMount(() => {
		createChart()
	})

	const addChartData = (data) => {
		const newDatasets = data.datasets
		const date = new Date(data.time * 1000)
		const minsec = date
			.toLocaleTimeString()
			.split(":")
			.slice(1, 3)
			.join(":")
		const time = `${minsec}.${date.getMilliseconds()}`

		chart.data.labels.push(time)
		newDatasets.forEach((newDataset) => {
			const index = data.datasets.findIndex(
				(e) => e.label == newDataset.label
			)
			chart.data.datasets[index].data.push(newDataset.data)
			chart.update()
		})
	}

	const toggleRecording = () => {
		if (recording) {
			socket.emit("session:pause")
			recording = false
		} else {
			socket.emit("session:resume")
			recording = true
		}
	}

	const socket = io(`ws://${location.hostname}:5000`, {
		reconnectionDelayMax: 10000,
	})

	socket.on("connect", () => {
		backendReady = true
		console.log(`Connected to: ${socket.id}`)
	})

	socket.on("disconnect", () => {
		backendReady = false
		console.log(`Disconnected from socket`)
	})

	socket.on("data:update", (data) => {
		if (recording === false) {
			return
		}
		console.log("Recieved data")
		console.log(data)
		addChartData(data)
		return
	})

	const newSession = () => {
		recording = false
		socket.emit("session:req:new")
	}

	socket.on("session:res:new", (data) => {
		session = data.session
		chart.destroy()
		createChart()
		recording = true
	})
</script>

<main>
	<div class="header">
		<h1>OBD Monitor</h1>
		<StatusBar {backendReady} />
	</div>
	<div class="ControlCenter">
		{#if session}
		<div class="information">
			<h2>Session #{session ? session : ""}</h2>
			<!-- <div class="statusInfo">
				<StatusIndicator ready={false} />
				<h2>OBD:</h2>
			</div> -->
		</div>
		<div class="controls">
			<button on:click={newSession}>New Session</button>
			<!-- <button>Delete Session</button> -->
			<button on:click={toggleRecording}
			>{recording ? "Pause" : "Resume"}</button
			>
		</div>
		{/if}
		<div class="graph">
			<canvas
			bind:this={chartCtx}
			width={400}
			height={400}
			class={session ? "" : "is-hidden"}
			/>
		</div>
	</div>
	<!-- {#if showModal}
		<Modal/>
	{/if} -->
</main>

<style lang="scss">
	canvas {
		&.is-hidden {
			visibility: hidden;
		}
	}

	p,
	h1,
	h2 {
		margin: 0;
	}

	.header h1 {
		margin: 0px;
	}

	.header {
		margin-bottom: 40px;
	}

	.ControlCenter {
		display: flex;
		flex-direction: column;
		gap: 20px;
		.information {
			display: flex;
			flex-direction: column;
			gap: 10px;
		}
		// .statusInfo {
		// 	display: flex;
		// 	align-items: center;
		// 	gap: 10px;
		// 	justify-content: center;
		// }
	}
</style>
