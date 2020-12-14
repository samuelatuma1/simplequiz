
            document.addEventListener('DOMContentLoaded',() =>{
               
                //Get dashboard 
                dashboard = document.querySelector('.nav_home')
                dashboard.onclick = function(){
                    
                    // Get navigation
                    nav = document.querySelector('#nav_house')
                    
                    //Conditional statement

                    //if it is not displayed
                      //Display
                    if(nav.style.display=='none'){
                        nav.style.animationName = 'expand';
                        nav.style.animationDuration = '1s';
                        nav.style.animationPlayState = 'forwards'
                        nav.addEventListener('animationend', function(){
                            nav.style.display = 'block';
                        })
                        nav.style.display = 'block';
                    }
                    //Else, if displayed, hide
                    else if(nav.style.display=='block'){
                        nav.style.animationName = 'contract';
                        nav.style.animationDuration = '1s';
                        nav.style.animationPlayState = 'forwards'
                        nav.addEventListener('animationend', function(){
                            nav.style.display = 'none';
                        })
                        
                    }

                    else{
                        nav.style.animationName = 'expand';
                        nav.style.animationDuration = '1s';
                        nav.style.animationPlayState = 'forwards'
                        nav.style.display = 'block';
                        nav.addEventListener('animationend', function(){
                            nav.style.display = 'block';
                        })
                        nav.style.display = 'block';
                    }

                }


                // If screen size is bigger than 800px, display the navigation
                function largeScreen(mediaScreen) {
                        nav = document.querySelector('#nav_house')
                        //If screen size is more than 800px
                        if (mediaScreen.matches) { // If media query matches
                                nav.style.animationName = 'expand';
                                nav.style.animationDuration = '1s';
                                nav.style.animationPlayState = 'forwards'
                                nav.style.display = 'block';
                                nav.addEventListener('animationend', function(){
                                nav.style.display = 'block';
                        })
                        nav.style.display = 'block';
                        } 
                        //else If screen size is less than 800px
                        else{
                            nav.style.animationName = 'contract';
                        nav.style.animationDuration = '1s';
                        nav.style.animationPlayState = 'forwards'
                        nav.addEventListener('animationend', function(){
                            nav.style.display = 'none';
                        })
                        }
                        
                        }

                        var x = window.matchMedia("(min-width: 800px)")
                        largeScreen(x) // Call listener function at run time
                        x.addListener(largeScreen) // Attach listener function on state changes
                                
            })