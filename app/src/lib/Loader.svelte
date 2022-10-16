<span class="Loader"></span>

<style lang="scss">
    @keyframes loader {
        0% {
            scale: 0;
            animation-timing-function: linear;
        }
    
        80% {
            scale: 1;
            animation-timing-function: linear;
        }
    
        100% {
            scale: 1.5;
            opacity: 0;
            animation-timing-function: linear;
        }
    }
    .Loader {
        display: block;
        height: 100px;
        width: 100px;
        border-radius: 100px;
        background-color: red;
        animation: loader 1s ease-out infinite;
    }
</style>
