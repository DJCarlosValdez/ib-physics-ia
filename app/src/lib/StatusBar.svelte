<script>
	import StatusIndicator from "./StatusIndicator.svelte"
    let backendReady
</script>

<div class="StatusBar">
    <StatusIndicator ready={backendReady}/>
    <p>Status: {backendReady ? "Ready" : "Not Ready"}</p>
</div>

<style lang="scss">
	.StatusBar {
		display: flex;
		align-items: center;
		gap: 10px;
		justify-content: center;

		p {
			font-size: 1.25rem;
		}
	}
</style>