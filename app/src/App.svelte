<script>
	import svelteLogo from "./assets/svelte.svg"
	import Counter from "./lib/Counter.svelte"
	import StatusBar from "./lib/StatusBar.svelte"
	import StatusIndicator from "./lib/StatusIndicator.svelte"
	import Chart from "chart.js/auto/auto.js"
	import { io } from "socket.io-client"
	import { onMount } from "svelte"

	let chart
	let backendReady = false
	let recording = false
	let deleteModal = false

	const data = {
		labels: [1, 2, 3, 4, 5],
		datasets: [
			{
				label: "My First Dataset",
				data: [0, 1, 2, 3, 4],
				borderColor: "#e22134",
				fill: false,
				tension: 0.1,
				// hoverOffset: 4,
				// borderWidth: 0,
			},
		],
	}

	const config = {
		type: "line",
		data: data,
		options: {
			borderRadius: "30",
			responsive: true,
			cutout: "95%",
			spacing: 2,
			plugins: {
				legend: {
					position: "bottom",
					display: true,
					labels: {
						usePointStyle: true,
						padding: 20,
						font: {
							size: 14,
						},
					},
				},
			},
		},
	}

	onMount(() => {
		const ctx = chart.getContext("2d")
		// @ts-ignore
		let myChart = new Chart(ctx, config)
	})

	const toggleRecording = () => {
		recording = recording ? false : true
	}

	// const socket = io("ws://localhost:8050", {
	// 	reconnectionDelayMax: 10000,
	// })

	// socket.on("connect", () => {
	// 	backendReady = true
	// 	console.log(`Connected to: ${socket.id}`)
	// })

	// socket.on("disconnect", () => {
	// 	backendReady = false
	// 	console.log(`Disconnected from socket`)
	// })
</script>

<main>
	<div class="header">
		<h1>OBD Monitor</h1>
		<StatusBar {backendReady} />
	</div>
	<div class="ControlCenter">
		<div class="information">
			<h2>Session #</h2>
			<div class="statusInfo">
				<StatusIndicator {backendReady} />
				<h2>OBD:</h2>
			</div>
		</div>
		<div class="controls">
			<button>New Session</button>
			<button>Delete Session</button>
			<button on:click={toggleRecording}
				>{recording ? "Stop" : "Start"}</button
			>
		</div>
		<div class="graph">
			<canvas bind:this={chart} width={400} height={400} />
		</div>
	</div>
	<div class="Modal">
		<div class="card-buffer">
			<div class="card">
				<h2>System Override</h2>
				<p>The system blocks this by default. Please confirm you wish to delete this session.</p>
				<div class="buttons">
					<button>Cancel</button>
					<button>Confirm</button>
				</div>
			</div>
		</div>
		<div class="modal-bg" />
	</div>
</main>

<style lang="scss">
	.Modal {
		position: absolute;
		height: 100%;
		width: 100%;
		top: 0;
		left: 0;
		.modal-bg {
			height: 100%;
			width: 100%;
			background-color: rgba(0, 0, 0, 0.5);
		}
		.card-buffer {
			position: absolute;
			height: 100%;
			width: 100%;
			display: flex;
			justify-content: center;
			align-items: center;
			.card {
				display: flex;
				flex-direction: column;
				text-align: left;
				gap: 10px;
				border-radius: 20px;
				position: absolute;
				display: flex;
				justify-content: center;
				width: 80%;
				background-color: #1a1a1a;
				color: white;
				padding: 20px;
			}

			@media (prefers-color-scheme: light) {
				.card {
					color: black;
					background-color: white;
				}
			}
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
		.statusInfo {
			display: flex;
			align-items: center;
			gap: 10px;
			justify-content: center;
		}
	}
</style>
