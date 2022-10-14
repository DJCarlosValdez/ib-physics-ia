<script>
	let ready
</script>

<span class={`statusIndicator ${ready ? "green" : "red"}`} />

<style lang="scss">
	@keyframes blink {
		0% {
			opacity: 0;
		}
		40% {
			opacity: 1;
		}
		60% {
			opacity: 1;
		}
		100% {
			opacity: 0;
		}
	}
    
	.statusIndicator {
		display: block;
		height: 16px;
		width: 16px;
		border-radius: 16px;
		background-color: white;

		animation: blink 2s ease-in-out infinite;

		&.red {
			background-color: #e22134;
		}

		&.green {
			background-color: #1db954;
		}
	}
</style>
